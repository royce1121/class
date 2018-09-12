from import_export import resources
from .models import Person, Person1

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person1