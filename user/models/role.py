from typing import Any, Dict

from django.db import models

from base.models.base_core import BaseCoreEntity





class Role(BaseCoreEntity):
    name = models.CharField( max_length=255,unique=True,verbose_name="name")
    display_name = models.CharField(max_length=255,verbose_name="Nom")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    admin_permission = models.BooleanField(default=False, verbose_name="Admin Permission")
    permissions = models.JSONField(null=True, blank=True, verbose_name="Permissions")
    field_permissions = models.JSONField(null=True, blank=True, verbose_name="Field Permissions")
    def build_ability_rules(self):
        # Example: This function would require further customization based on your permissions logic
        rules = []
        if self.permissions:
            for key, value in self.permissions.items():
                if value is True:
                    rules.append({"action": "all", "subject": key})
                elif isinstance(value, dict):
                    for action_key, action_value in value.items():
                        if action_value is True:
                            rule = {"action": action_key, "subject": key}
                            rule = self.apply_field_permissions(rule)
                            rules.append(rule)
        if self.admin_permission:
            rules.append({"action": "manage", "subject": "all"})
        return rules

    def apply_field_permissions(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        if not self.field_permissions:
            return rule
        subject_permissions = self.field_permissions.get(rule["subject"], {})
        if rule["action"] == "read":
            rule["fields"] = subject_permissions.get("read", [])
        elif rule["action"] in {"create", "edit"}:
            rule["fields"] = subject_permissions.get("edit", [])
        return rule

    def to_json(self):
        # Converts the model instance to a serializable dictionary
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "is_active": self.is_active,
            "admin_permission": self.admin_permission,
            "permissions": self.permissions,
            "field_permissions": self.field_permissions,
        }
    class Meta:
        app_label = 'user' 
