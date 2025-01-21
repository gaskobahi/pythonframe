# accounts/management/commands/assign_role_to_user.py
from django.core.management.base import BaseCommand

from user.models.role import Role
from user.models.user import User

class Command(BaseCommand):
    help = "Assign a role to a user"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="The username of the user")
        parser.add_argument('role', type=str, help="The name of the role to assign")

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        role_name = kwargs['role']

        try:
            # Fetch the user
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User '{username}' does not exist."))
            return

        try:
            # Fetch the role
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Role '{role_name}' does not exist."))
            return

        # Assign the role to the user
        user.role = role
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"L'utilisateur '{user.username}' a maintenant le rôle : '{role.name}'"
        ))
