from .enums import AbilityActionEnum, AbilitySubjectEnum


def define_abilities_for(user):
    print('sdsdsdsdsd',user)
    """
    Génère les règles d'abilities pour un utilisateur donné.
    """
    # Exemple de structure des permissions
    permissions = {
        "Article": {"read": True, "create": True, "delete": False},
        "Branch": True,  # L'utilisateur peut tout faire sur "Branch"
    }

    field_permissions = {
        "Article": ["title", "content"],  # Champs accessibles
    }

    admin_permission = user.get('is_superuser')
    # Génère les règles
    rules = build_ability_rules(user.get('role').get('permissions'), user.get('role').get('field_permissions'), admin_permission)
    return rules


def build_ability_rules(permissions:object={}, field_permissions=None, admin_permission=False):
    """
    Génère des règles CASL-friendly basées sur les permissions et d'autres paramètres.

    :param permissions: Un dictionnaire représentant les permissions { "subject": { "action": True } }
    :param field_permissions: Un dictionnaire optionnel pour les permissions par champ.
    :param admin_permission: Booléen indiquant si l'utilisateur a des permissions administratives.
    :return: Liste de règles CASL-friendly.
    """
    rules = []
    
    # Parcourt les permissions générales
    for subject, actions in permissions.items():
        if actions is True:  # Si "all" est autorisé pour le sujet
            rules.append({"action": AbilityActionEnum.manage, "subject": subject})
        elif isinstance(actions, dict):  # Si les actions sont détaillées
            for action, is_allowed in actions.items():
                if is_allowed:
                    rule = {"action": action, "subject": subject}
                    # Applique les permissions par champ
                    rule = apply_field_permissions(rule, field_permissions)
                    rules.append(rule)

    # Appliquer les permissions d'admin si définies
    rules = apply_admin_permission(rules, admin_permission)
    print('dsdsdddsd',admin_permission)

    return rules


def apply_field_permissions(rule, field_permissions):
    """
    Applique les permissions spécifiques à certains champs à une règle donnée.

    :param rule: La règle actuelle.
    :param field_permissions: Dictionnaire des permissions par champ.
    :return: La règle modifiée.
    """
    if not field_permissions:
        return rule

    # Exemple : Ajouter des permissions spécifiques par champ si applicable
    rule["fields"] = field_permissions.get(rule["subject"], None)
    return rule


def apply_admin_permission(rules, admin_permission):
    """
    Ajoute une règle d'administrateur si l'utilisateur a des permissions admin.

    :param rules: Liste des règles existantes.
    :param admin_permission: Booléen indiquant les permissions admin.
    :return: Liste mise à jour des règles.
    """
    if admin_permission:
        rules.append({"action": AbilityActionEnum.manage, "subject": AbilitySubjectEnum.all})
    return rules