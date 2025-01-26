from rest_framework.permissions import BasePermission
from base.enums import AbilityActionEnum, AbilitySubjectEnum
from common.abilities.abilities import define_abilities_for
from rest_framework.exceptions import AuthenticationFailed

class AbilityPermission(BasePermission):
    """
    Autorisation personnalisée basée sur les abilities définies pour l'utilisateur.
    """

    def has_permission(self, request, view):
        resource_action = view.get_resource_action()  # Retrieve action
        resource_subject = view.resource_subject  # Retrieve subject
        if not resource_action or not resource_subject:
            return False
        
        abilities = define_abilities_for(request.authUser.get('user'))
        for ability in abilities["can"]:
            # Vérifie si l'utilisateur peut effectuer l'action sur le resource
            if ability.get("action") == AbilityActionEnum.manage and ability.get("subject") == AbilitySubjectEnum.all:
                return True  # User has global permissions                return True

            # Match ability with action and subject
            if ability.get("action") == AbilityActionEnum[resource_action] and ability.get("subject") == resource_subject:
                return True  # User has permission for the action on the subject
        raise AuthenticationFailed("Permission non autorisée.")

