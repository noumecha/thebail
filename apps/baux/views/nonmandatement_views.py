from django.views.generic import TemplateView
from web_project import TemplateLayout
from ..models import *
from ..forms import *
from .views import *

# Non-Mandatement Class and views :
class Non_MandatementView(BaseCRUDView):
    model = Non_Mandatement
    form_class = NonMandatementForm
    list_route = 'non_mandatement_list'
    list_template = 'baux/non_mandatement_list.html'
    partial_template = 'baux/partials/non_mandatements_partial.html'
    context_object_name = 'non_mandatements'
    search_fields = ['Avenant__Ref_Avenant']

class AvenantsView(BaseCRUDView):
    model = Avenants
    form_class = AvenantsForm
    list_route = 'avenant_list'
    list_template = 'baux/avenant_list.html'
    partial_template = 'baux/partials/avenants_partial.html'
    context_object_name = 'avenants'
    search_fields = ['Ref_Avenant']

class ConsultationView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["datas"] = []
        return context
    
class StatsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["datas"] = []
        return context