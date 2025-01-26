from rest_framework.permissions import BasePermission

class AbilityPermission(BasePermission):
    """
    DRF permission class to enforce CASL rules.
    """

    def __init__(self, ability_rules):
        self.ability_rules = ability_rules

    def has_permission(self, request, view):
        """
        Check if the user has permission based on ability rules.
        """
        action = view.action  # Example: 'list', 'create', etc.
        subject = view.get_view_name()  # Map this to your subject (e.g., 'User')
        for rule in self.ability_rules:
            if rule["action"] == action and rule["subject"] == subject:
                return True
        return False