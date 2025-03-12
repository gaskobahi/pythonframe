# serializers.py
from rest_framework import serializers


class StockMovementTotalSerializer(serializers.Serializer):
    total_input = serializers.IntegerField(required=False)
    total_output = serializers.IntegerField(required=False)
    total_quantity = serializers.IntegerField(required=False)
    total_bags_input = serializers.IntegerField(required=False)
    total_bags_output = serializers.IntegerField(required=False)
    total_bags_quantity = serializers.IntegerField(required=False)
    total_quantity_kg_lbs = serializers.IntegerField(required=False)
    total_kor = serializers.IntegerField(required=False)


class StockMovementDetailSerializer(serializers.Serializer):
    month = serializers.CharField(required=False)
    package_lot = serializers.CharField(required=False)
    variant_code = serializers.CharField(required=False)
    article_number = serializers.CharField(required=False)
    


    
    # Mouvements généraux
    initial_stock = serializers.FloatField(required=False)
    purchase = serializers.FloatField(required=False)
    production = serializers.FloatField(required=False)
    consumption = serializers.FloatField(required=False)
    positive_adjustment = serializers.FloatField(required=False)
    sales = serializers.FloatField(required=False)
    negative_adjustment = serializers.FloatField(required=False)
    final_stock = serializers.FloatField(required=False)

    # Mouvements par lot de paquet
    input = serializers.FloatField(required=False)
    output = serializers.FloatField(required=False)
    total_quantity = serializers.FloatField(required=False)
    total_quantity_kg_lbs =serializers.FloatField(required=False)
    bags_input = serializers.FloatField(required=False)
    bags_output = serializers.FloatField(required=False)
    total_bags_quantity = serializers.FloatField(required=False)
    sale_current_year = serializers.FloatField(required=False)
    sale_count_previous_year = serializers.FloatField(required=False)

    
    kor_reception = serializers.FloatField(required=False)


class StockMovementSerializer(serializers.Serializer):
    variant_code = serializers.CharField()
    article_number = serializers.CharField()
    package_lot=serializers.CharField(allow_null=True,required=False)
    type_ecriture=serializers.CharField(allow_null=True,)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    data = StockMovementDetailSerializer(many=True)  # Liste des mouvements par mois
    totals=StockMovementTotalSerializer(allow_null=False)



