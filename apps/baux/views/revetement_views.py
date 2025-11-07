from .views_base import BaseCRUDView
from ..models import RevetementExts, RevetementInts
from ..forms import RevetementExtsForm, RevetementIntsForm

# revetements views
class RevetementExtsView(BaseCRUDView):
    model = RevetementExts
    form_class = RevetementExtsForm
    list_route = 'revetementext_list'
    list_template = 'baux/revetementext_list.html'
    partial_template = 'baux/partials/revetementexts_partial.html'
    context_object_name = 'revetementexts'
    search_fields = ['libelle']

class RevetementIntsView(BaseCRUDView):
    model = RevetementInts
    form_class = RevetementIntsForm
    list_route = 'revetementint_list'
    list_template = 'baux/revetementint_list.html'
    partial_template = 'baux/partials/revetementints_partial.html'
    context_object_name = 'revetementints'
    search_fields = ['libelle']
