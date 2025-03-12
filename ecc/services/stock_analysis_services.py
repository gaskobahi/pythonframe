# myapp/views.py
from collections import defaultdict
from datetime import datetime
from django.db.models.functions import Cast, ExtractYear, ExtractMonth, Concat
from django.db.models import Sum, Value, CharField,DateField

from regex import F
from base.enums import ArticleEnum, BCKVariantEnum, CKFGVariantEnum, CRCNVariantEnum
from capro_data_analyse import settings
from ecc.models.ecc import Ecc
from django.db.models.functions import Round,Coalesce
from django.db.models import Sum, Case, When, Value, IntegerField,F,Avg,FloatField,Func,Q

# Custom function to replace ',' with '.'


# 🔹 Transaction types pour réutilisation
TRANSACTION_TYPES = {
    'positive': ['Achat', 'Positif (ajust.)', 'Production'],
    'negative': ['Consommation', 'Vente', 'Négatif (ajust.)']
}




class ReplaceComma(Func):
    function = "REPLACE"
    template = "%(function)s(%(expressions)s, ',', '.')"

# Custom function to remove spaces
class RemoveSpaces(Func):
    function = "REPLACE"
    template = "%(function)s(%(expressions)s, ' ', '')"


# 🔹 Fonction pour filtrer la base de données
def filter_query_set(queryset,params,is_for_stock_mvt=False):
    if  is_for_stock_mvt:
        """ Applique les filtres communs à la base de données """
        queryset = queryset.annotate(
            date_as_date=Cast('accounting_date', DateField())
        ).filter(date_as_date__range=[params["start_date"], params["end_date"]])
        queryset = queryset.annotate(
                year=Cast(ExtractYear('date_as_date'), CharField()),
                month=Cast(ExtractMonth('date_as_date'), CharField()),
                year_month=Concat('year', Value('-'), 'month')
        )
    else:
        queryset = queryset.annotate(
            date_as_date=Cast('accounting_date', DateField())
        ).filter(
            Q(date_as_date__lte=params["start_date"]) |  # Tout ce qui précède start_date
            Q(date_as_date__range=[params["start_date"],params["end_date"] ])  # Intervalle classique
        )
    
        

    if params["package_lot"]:
            queryset = queryset.filter(package_lot__in=params["package_lot"])
    if params["article_numbers"]:
        queryset = queryset.filter(article_number__in=params["article_numbers"])
    if params["variant_code"]:
        queryset = queryset.filter(variant_code=params["variant_code"])
    if params["type_ecriture"]:
        queryset = queryset.filter(type_ecriture__in=params["type_ecriture"])
    

    return queryset


def aggregate_package_and_lot(entity:Ecc,is_for_stock_mvt:bool):
        queryset = entity.objects.annotate(
            package_lot=Case(
                When(~Q(package_number=""), then=F('package_number')),
                When(~Q(lot_number=""), then=F('lot_number')),
                default=None,
                output_field=CharField(),
            ),
            quantity_in_bag=Cast(F('quantity_in_sac'), FloatField())
        ).filter(package_lot__isnull=False)
        #mouve!et de stock pas concerné par ce filtre
        if not is_for_stock_mvt:
            queryset=queryset.filter(is_open="VRAI")

        return queryset
  # 🔹 Utilitaires pour récupérer et formater les paramètres de requête

def get_query_params(request):
    """ Récupère et normalise les paramètres de la requête """
    today = datetime.today()
    return {
        "start_date": request.GET.get('start_date', today.replace(month=12, day=31, year=today.year - 1).strftime('%Y-%m-%d')),
        "end_date": request.GET.get('end_date', today.strftime('%Y-%m-%d')),
        "article_numbers": request.GET.getlist('article_number'),  # Toujours sous forme de liste
        "type_ecriture": request.GET.getlist('type_ecriture'),
        "variant_code": request.GET.get('variant_code'),
        "package_lot": request.GET.getlist('package_lot')
    }

# 🔹 Fonction d'agrégation des stocks
def aggregate_stock_data(entity:Ecc, params):
    queryset = entity.annotate(date_as_date=Cast('accounting_date', DateField()))
    """ Calcule le stock initial et final par article """
    historique_avant = queryset.filter(date_as_date__lt=params["start_date"])
    if params["article_numbers"]:
        historique_avant = historique_avant.filter(article_number__in= params["article_numbers"])
    if  params["variant_code"]:
        historique_avant = historique_avant.filter(variant_code=params["variant_code"])
    if  params["package_lot"]:
            historique_avant = historique_avant.filter(package_lot__in=params["package_lot"])

    # Calcul du stock initial par article
    stock_initial_par_article = {
        article: (
            sum(historique_avant.filter(article_number=article, type_ecriture=typ).aggregate(Sum('quantity'))['quantity__sum'] or 0
                for typ in TRANSACTION_TYPES['positive'])
            - sum(abs(historique_avant.filter(article_number=article, type_ecriture=typ).aggregate(Sum('quantity'))['quantity__sum'] or 0)
                for typ in TRANSACTION_TYPES['negative'])
        )
        for article in params["article_numbers"]
    }


    # 🔹 Apply filters for main dataset
    queryset=filter_query_set(queryset,params,is_for_stock_mvt=True)
    
    # Regroupement des données
    data_grouped = queryset.values('article_number', 'type_ecriture','year_month').annotate(total_quantite=Sum('quantity')).order_by('article_number', 'type_ecriture')
# 🔹 Get unique months
    mois_uniques = sorted(set(data_grouped.values_list('year_month', flat=True)), key=lambda x: (int(x[:4]), int(x[5:])))

    # Calcul des stocks mois par mois

        # 📊 Compute stock per article
    stock_table = defaultdict(list)
    for mois in mois_uniques:
        for article in  params["article_numbers"]:
            # Create a dict with transaction types and their quantities
            data_mois = {item['type_ecriture']: item['total_quantite'] for item in data_grouped.filter(year_month=mois, article_number=article)}

            # Calculate stock final
            stock_initial = stock_initial_par_article[article]
            stock_final = stock_initial + sum(data_mois.get(t, 0) for t in TRANSACTION_TYPES['positive']) - sum(abs(data_mois.get(t, 0)) for t in TRANSACTION_TYPES['negative'])

            # Store data
            stock_table[article].append({
                'month': mois,
                'initial_stock': stock_initial,
                'purchase': data_mois.get('Achat', 0),
                'production': data_mois.get('Production', 0),
                'consumption': data_mois.get('Consommation', 0),
                'positive_adjustment': data_mois.get('Positif (ajust.)', 0),
                'sales': data_mois.get('Vente', 0),
                'negative_adjustment': data_mois.get('Négatif (ajust.)', 0),
                'final_stock': stock_final
            })

            # Update stock for next month
            stock_initial_par_article[article] = stock_final

    # 📌 Prepare final response
    resultat_final = [
        {
            'article_number': article,
            'package_lot': params['package_lot'],
            'variant_code': params['variant_code'],
            'start_date': params['start_date'],
            'end_date': params['end_date'],
            'data': data,
            'totals':{}
        }
        for article, data in stock_table.items()
    ]

    return resultat_final

   
def get_workflow_not_for_stockmvt(entity:Ecc,params):
        # Si on inclut les numéros de lot/package
    queryset = aggregate_package_and_lot(entity,True)
    # 🔹 Filter dataset from database
    queryset = queryset.annotate(quantity_in_bag=Cast(RemoveSpaces(F('quantity_in_sac')), FloatField()))
    # 🔹 Corriger et appliquer le filtre sur la date
    queryset = filter_query_set(queryset,params,False)
    return queryset

# 🔹 Utilitaires pour récupérer et formater les paramètres de requête
def convert_variant_quantity_in_kg(quantityBag,variantCode,article_number):
    quantityKg=quantityBag
    if variantCode in CKFGVariantEnum and article_number == ArticleEnum.CKFG:
        quantityKg=round((quantityBag*settings.CONVERSION_FACTOR_CKFG),2)
    if variantCode in BCKVariantEnum  and article_number == ArticleEnum.CKFG:
        quantityKg=round((quantityBag*settings.CONVERSION_FACTOR_BCK),2)
    if variantCode in CRCNVariantEnum and article_number == ArticleEnum.CRCN:
        quantityKg=round((quantityBag*settings.CONVERSION_FACTOR_CRCN),2)
    return quantityKg or 0










def get_stockmovement_service(request):
    params = get_query_params(request)
    # Si on inclut les numéros de lot/package
    queryset = aggregate_package_and_lot(Ecc,True)
    stock_table = aggregate_stock_data(queryset, params)
    return stock_table


def get_mvt_by_package_lot_number_service(request):
    params = get_query_params(request)
    # Si on inclut les numéros de lot/package
    queryset=get_workflow_not_for_stockmvt(Ecc,params)
        # Agrégation des données par article
    queryset = queryset.values("package_lot").annotate(
            input=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['positive'], then=F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            output=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['negative'], then=F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_quantity=Coalesce(
                Sum(
                    Case(
                        When(type_ecriture__in=TRANSACTION_TYPES['positive'], then=F('quantity')),
                        When(type_ecriture__in=TRANSACTION_TYPES['negative'], then=F('quantity')),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ), Value(0)
            ),
            bags_input=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['positive'], then=F('quantity_in_bag')),
                    default=Value(0),
                    output_field=FloatField()
                )
            ),
            bags_output=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['negative'], then=-F('quantity_in_bag')),
                    default=Value(0),
                    output_field=FloatField()
                )
            ),
            total_bags_quantity=Sum("quantity_in_bag"),
            kor_reception=Round(Avg("kor_by_reception"), 2),
        )
    total_input = 0
    total_output = 0
    total_quantity = 0
    total_quantity_kg_lbs = 0
    total_bags_input = 0
    total_bags_output = 0
    total_bags_quantity = 0
    for item in queryset:
        item_input = item.get("input", 0),
        item_output = item.get("output", 0),
        item_total_quantity = item.get("total_quantity", 0)
        item_bags_input = item.get("bags_input", 0)
        item_bags_output = item.get("bags_output", 0)
        item_bags_quantity=item.get('total_bags_quantity',0)   
        #print('poooooooo',item_input.replace(",", ""))

            # Ajout des valeurs aux totaux
        #total_input += Cast(RemoveSpaces(item_input), FloatField())
        #total_output += item_output
        #total_quantity += item_total_quantity
        #total_bags_input += item_bags_input
        #total_bags_output += item_bags_output
        #total_bags_quantity += item_bags_quantity

            # 📌 Résumé total
        total_summary = {
            "total_input": total_input,
            "total_output": total_output,
            "total_quantity": total_quantity,
            "total_quantity_kg_lbs": total_quantity_kg_lbs,
            "total_quantity_kg_lbs": total_bags_input,
            'total_bags_output':total_bags_output,
            'total_bags_quantity':total_bags_quantity
        }


    # 📌 Prepare final response
    resultat_final = [
        {
            'package_lot':params['package_lot'],
            'variant_code': params['variant_code'],
            'article_number':params['article_numbers'],
            'type_ecriture':params['type_ecriture'],
            'start_date':params['start_date'],
            'end_date':params['end_date'],
            'data': queryset,
            'totals':total_summary
        }
    ]

    return resultat_final


def get_mvt_by_variant_code_service(request):
    params = get_query_params(request)
    queryset=get_workflow_not_for_stockmvt(Ecc,params)
         # Agrégation des données par article
    queryset = queryset.values("variant_code","article_number").annotate(
            input=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['positive'], then=F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            output=Sum(
                Case(
                    When(type_ecriture__in=TRANSACTION_TYPES['negative'], then=F('quantity')),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_quantity=Coalesce(
                Sum(
                    Case(
                        When(type_ecriture__in=TRANSACTION_TYPES['positive'], then=F('quantity')),
                        When(type_ecriture__in=TRANSACTION_TYPES['negative'], then=F('quantity')),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ), Value(0)
            ),
            
        )
    results = []
    total_input = 0
    total_output = 0
    total_quantity = 0
    total_quantity_kg_lbs = 0
    # 🔹 Ajouter `total_quantity_kg_lbs` à chaque élément
    for item in queryset:
        item_input = item.get("input", 0)
        item_output = item.get("output", 0)
        item_total_quantity = item.get("total_quantity", 0)

        item_quantity_kg =convert_variant_quantity_in_kg(item.get('total_quantity'),item.get('variant_code'),item.get('article_number'))
        
         # Ajout des valeurs aux totaux
        total_input += item_input
        total_output += item_output
        total_quantity += item_total_quantity
        total_quantity_kg_lbs += item_quantity_kg

        item_data = {**item, "total_quantity_kg_lbs": total_quantity_kg_lbs}
        results.append(item_data)
        
         # 📌 Résumé total
        total_summary = {
            "total_input": total_input,
            "total_output": total_output,
            "total_quantity": total_quantity,
            "total_quantity_kg_lbs": total_quantity_kg_lbs
        }

    # 📌 Prepare final response
    resultat_final = [
        {
            'package_lot':params['package_lot'],
            'variant_code': params['variant_code'],
            'article_number':params['article_numbers'],
            'type_ecriture':params['type_ecriture'],
            'start_date':params['start_date'],
            'end_date':params['end_date'],
            'data': results,
            'totals': total_summary,  
        }
    ]

    print('klklkl',resultat_final)
    return resultat_final

  

    
 