from django.contrib import admin
from .models import Locataire
from .models import TypePersonne

# Register your models here.
admin.site.register(Locataire)
admin.site.register(TypePersonne)