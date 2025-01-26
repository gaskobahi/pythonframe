
from base.enums import AbilityActionEnum, AbilitySubjectEnum


def apply_field_permissions(rule, field_permissions):
    """Modify the rule to include field-level restrictions."""
    # Example: Add field-specific logic here if needed
    return rule

def apply_admin_permission(rules, admin_permission):
    """Grant full access if the user has admin permissions."""
    if admin_permission:
        rules.append({"action": AbilityActionEnum.manage, "subject": AbilitySubjectEnum.all})
    return rules

def build_ability_rules(permissions, field_permissions=None, admin_permission=None):
    """
    Convert permissions into CASL rules.
    Args:
        permissions (dict): User's permissions.
        field_permissions (dict): Optional field-level permissions.
        admin_permission (bool): Flag to enable admin access.
    Returns:
        list: CASL-compatible rules.
    """
    rules = []
    for subject, actions in permissions.items():
        if actions is True:  # Grant all actions for a subject
            rules.append({"action": AbilityActionEnum.manage, "subject": subject})
        elif isinstance(actions, dict):  # Process detailed permissions
            for action, is_allowed in actions.items():
                if is_allowed:
                    rule = {"action": action, "subject": subject}
                    rule = apply_field_permissions(rule, field_permissions)
                    rules.append(rule)
    rules = apply_admin_permission(rules, admin_permission)
    return rules

def ability_transform(rules):
    """
    Transforms rules into the required CASL format (optional customization).
    Args:
        rules (list): List of action/subject rules.
    Returns:
        dict: Transformed rules in CASL-compatible structure.
    """
    return {"can": rules}