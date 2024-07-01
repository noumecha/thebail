from django.views.generic import TemplateView
from web_project import TemplateLayout
from .models import Bailleur, AyantDroit
from django.shortcuts import render, redirect
from .forms import BailleurForm, AyantDroitForm

class bailleurView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        #A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["bailleurs"] = Bailleur.objects.all()
        context["bailleur_form"] = BailleurForm
        context["ayant_droit_form"] = AyantDroitForm
        return context
    
    def post(self, request, *args, **kwargs):
        #if 'bailleur_form' in request.POST:
        bailleur_form = BailleurForm(request.POST)
        if bailleur_form.is_valid():
            bailleur_form.save()
            return redirect('bailleur-list')
        else:
            context = self.get_context_data()
            context["bailleur_form"] = bailleur_form
            return self.render_to_response(context)
        #elif 'ayant_droit_form' in request.POST:
        #    ayant_droit_form = AyantDroitForm(request.POST)
        #    if form.is_valid():
        #        form.save()
        #        return redirect('bailleur-list')
        #    else:
        #        context = self.get_context_data()
        #        context["ayant_droit_form"] = ayant_droit_form
        #        return self.render_to_response(context)