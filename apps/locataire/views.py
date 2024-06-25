from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render
from .models import Locataire, TypePersonne

# Create your views here.
class locataireView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["locataires"] = Locataire.objects.all()
        return context