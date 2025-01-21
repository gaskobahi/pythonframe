# accounts/management/commands/create_default_role.py
from django.core.management.base import BaseCommand

from user.models.role import Role


class Command(BaseCommand):
    help = "Supprime le rôle par défaut s'il existe et le recrée"

    def handle(self, *args, **kwargs):
        default_role_name = "Administrator"
        default_role_displayName = "Administrator"
        default_role_description = "Default admin role with all privileges."

        # Check if the default role exists
        role = Role.objects.filter(name=default_role_name).first()
        if role:
            role.delete()  # Delete the existing role
            self.stdout.write(self.style.WARNING(f"Le rôle '{default_role_name}' a été supprimé."))

        # Create a new role
        Role.objects.create(
            name=default_role_name,
            display_name=default_role_displayName,
            description=default_role_description,
        )
        self.stdout.write(self.style.SUCCESS(f"Rôle recréé : {default_role_name}"))