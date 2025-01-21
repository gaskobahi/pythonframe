# accounts/management/commands/create_default_user.py
from django.core.management.base import BaseCommand

from user.models.user import User  

class Command(BaseCommand):
    help = "Supprime l'utilisateur par défaut s'il existe et le recrée avec un mot de passe"

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@gmail.com"
        default_password = "admin"

        # Vérifie si l'utilisateur existe
        user = User.objects.filter(username=username).first()
        if user:
            user.delete()  # Supprime l'utilisateur existant
            self.stdout.write(self.style.WARNING(f"L'utilisateur {username} a été supprimé."))

        # Crée un nouvel utilisateur
        new_user = User.objects.create(
            username=username,
            email=email,
        )
        new_user.set_password(default_password)
        self.stdout.write(self.style.SUCCESS(f"Utilisateur recréé : {username} avec mot de passe '{default_password}'"))