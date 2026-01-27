from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from web_project import TemplateLayout
from django.template.loader import render_to_string
from ..models import *
from ..forms import *
from .views import *
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa


# for adding contrat type
class TypeContratView(BaseCRUDView):
    model = TypeContrats
    form_class = TypeContratsForm
    list_route = 'typecontrat_list'
    list_template = 'baux/typecontrat_list.html'
    partial_template = 'baux/partials/typecontrats_partial.html'
    context_object_name = 'typecontrats'
    search_fields = ['libelle', 'description']

class PeriodiciteReglementView(BaseCRUDView):
    model = PeriodiciteReglement
    form_class = PeriodiciteReglementForm
    list_route = 'periodiciterel_list'
    list_template = 'baux/periodiciterel_list.html'
    partial_template = 'baux/partials/periodiciterel_partial.html'
    context_object_name = 'periodiciterels'
    search_fields = ['libelle', 'description']

# contrat view
class ContratView(TemplateView):
    #predefined functiion
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["contratList"] = Contrats.objects.all().order_by('-Date_creation')
        pk = kwargs.get('pk', None)
        if pk:
            contrat = get_object_or_404(Contrats, pk=pk)
            form = ContratsForm(instance=contrat)
        else:
            form = ContratsForm()
        context["form"] = form
        context["is_update"] = pk is not None
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            contrat = get_object_or_404(Contrats, pk=pk)
            contrat_form = ContratsForm(request.POST, instance=contrat)
        else:
            contrat_form = ContratsForm(request.POST, request.FILES)

        if contrat_form.is_valid():
            contrat_form.save()
            return redirect('baux:contrat_list')
        else:
            context = self.get_context_data(pk=pk)
            context["form"] = contrat_form
            return self.render_to_response(context)

    def print_contrat(request, pk):
        # fetch content from db and load template context
        contrat = get_object_or_404(Contrats, pk=pk)
        context = {"contrat" : contrat}
        html = render_to_string("baux/docs/contrat_doc.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="f"contrat_{contrat.Ref_contrat}".pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response

class ContratUpdateView(UpdateView):
    model = Contrats
    form_class = ContratsForm
    template_name = 'baux/contrat.html'
    success_url = reverse_lazy('baux:contrat_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = self.get_form()
        return context

class ContratDeleteView(DeleteView):
    model = Contrats
    template_name = 'baux/contrat_delete.html'
    success_url = reverse_lazy('baux:contrat_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = ContratsForm()
        return context
