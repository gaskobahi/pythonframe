import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from base.models.base_core import BaseCoreEntity
from user.models.role import Role
from django.contrib.auth.hashers import make_password,check_password

class User(AbstractUser,BaseCoreEntity):
    
    username = models.CharField(max_length=150,unique=True,verbose_name=("Nom d'utilisateur"))
    password = models.CharField(max_length=128,null=True,blank=True,verbose_name=("Mot de passe"))
    is_active = models.BooleanField(default=True,verbose_name=("Compte actif"))
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,related_name="users",verbose_name=("Rôle"))
    last_access = models.UUIDField(default=uuid.uuid4)


    def set_new_password(self, password: str) -> str:
        return self.set_password(password)

    def check_password(self, password: str) -> bool:
        if not self.password:
            return False
        return check_password(password, self.password)

    def to_json(self):
        """
        Convert the user instance into a serializable dictionary.
        """
        return {
            "username": self.username,
            "is_active": self.is_active,
            "role": self.role.name if self.role else None,
            "last_access": self.last_access.id if self.last_access else None,
        }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return self.role.name
    
    class Meta:
        app_label = 'user' 
