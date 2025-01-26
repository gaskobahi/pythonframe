import json
from typing import Dict, List, Any


class AbilityService:
    """
    A service for building and transforming ability rules based on permissions.
    """

    @staticmethod
    def build_ability_rules(permissions: Dict[str, Dict[str, bool]]) -> List[Dict[str, str]]:
        """
        Constructs a list of ability rules from a permissions dictionary.

        :param permissions: Dictionary of permissions, where keys are subjects (e.g., "User")
                            and values are dictionaries of actions (e.g., {"read": True}).
        :return: List of rules in the format [{"action": "read", "subject": "User"}, ...].
        :raises ValueError: If permissions are improperly structured.
        """
        if not isinstance(permissions, dict):
            raise ValueError("Permissions must be a dictionary of subjects and actions.")

        ability_rules = []
        for subject, actions in permissions.items():
            if not isinstance(actions, dict):
                raise ValueError(f"Actions for subject '{subject}' must be a dictionary.")
            for action, is_allowed in actions.items():
                if is_allowed:  # Only include allowed actions
                    ability_rules.append({"action": action, "subject": subject})

        return ability_rules

    @staticmethod
    def ability_transform(rules: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Transforms a list of rules into a CASL-compatible structure.

        :param rules: List of rules in the format [{"action": "read", "subject": "User"}, ...].
        :return: Transformed dictionary with a "can" key.
        """
        if not isinstance(rules, list):
            raise ValueError("Rules must be a list of dictionaries.")
        return {"can": rules}

    @classmethod
    def process_permissions(cls, permissions: Dict[str, Dict[str, bool]]) -> Dict[str, Any]:
        """
        High-level method to build and transform ability rules in one step.

        :param permissions: Dictionary of permissions.
        :return: Transformed CASL-compatible dictionary.
        """
        rules = cls.build_ability_rules(permissions)
        return cls.ability_transform(rules)


# Example usage
if __name__ == "__main__":
    # Example permissions data
    permissions = {
        "User": {"read": True, "create": True, "edit": False, "delete": True},
        "Branch": {"read": True, "create": True, "edit": True, "delete": False, "stream": True},
        "Product": {"read": True, "create": False, "edit": True, "delete": True}
    }

    # Process permissions
    service = AbilityService()
    transformed_rules = service.process_permissions(permissions)

    # Print the result
    print(json.dumps(transformed_rules, indent=4))