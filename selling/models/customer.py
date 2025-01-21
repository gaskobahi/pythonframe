# myapp/models.py



from common.models.core_person_entity import PersonCoreEntity


class Customer(PersonCoreEntity):
   
    def __str__(self):
        return self.first_name