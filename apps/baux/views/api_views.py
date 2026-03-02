from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from ..models import *

class Select2SearchView(View):
    """
    Classe générique pour les recherches Select2

    Utilisation :
    class MyCustomSearch(Select2SearchView):
        model = MyModel
        search_fields = ['field1', 'field2']
        result_fields = {'id': 'id', 'text': 'name'}
    """
    model = None
    search_fields = []
    page_size = 30
    order_by = None

    # Format Select2
    id_field = None
    text_template = None
    extra_fields = []
    show_all_when_empty = False

    def get_queryset(self, search_term):
        if not search_term and self.show_all_when_empty:
            return self.model.objects.all()

        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": search_term})
        return self.model.objects.filter(q)

    def format_result(self, obj):
        text = self.text_template.format(**obj.__dict__)
        result = {
            "id": getattr(obj, self.id_field),
            "text": text
        }

        for field in self.extra_fields:
            result[field.lower()] = getattr(obj, field)

        return result

    def get(self, request):
        search_term = request.GET.get("q", "")
        page = int(request.GET.get("page", 1))

        qs = self.get_queryset(search_term)

        if self.order_by:
            qs = qs.order_by(self.order_by)

        start = (page - 1) * self.page_size
        end = start + self.page_size
        total = qs.count()

        objects = qs[start:end]

        return JsonResponse({
            "results": [self.format_result(obj) for obj in objects],
            "pagination": {"more": end < total}
        })

class AgentMatriculeSelect2(Select2SearchView):
    model = AgentCollecte
    search_fields = ["Matricule"]
    id_field = "Matricule"
    text_template = "{Matricule}"
    order_by = "Matricule"

class AgentNomSelect2(Select2SearchView):
    model = AgentCollecte
    search_fields = ["Matricule", "Nom", "Prenom"]
    id_field = "Matricule"
    text_template = "{Nom} {Prenom}"
    extra_fields = ["Matricule"]
    order_by = "Matricule"

class PaysSelect2(Select2SearchView):
    model = Pays
    search_fields = ["LibelleFR", "AbreviationFr"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class RegionSelect2(Select2SearchView):
    model = Regions
    search_fields = ["Libelle","code","AbreviationFr"]
    id_field = "pk"
    text_template = "{Libelle} ({AbreviationFr})"
    extra_fields = []
    order_by = "Libelle"

class DepartementSelect2(Select2SearchView):
    model = Departements
    search_fields = ["LibelleFR","AbreviationFr","code"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class ArrondissemntSelect2(Select2SearchView):
    model = Arrondissemements
    search_fields = ["LibelleFR","code","AbreviationFr"]
    id_field = "pk"
    text_template = "{LibelleFR} ({AbreviationFr})"
    extra_fields = []
    order_by = "LibelleFR"

class AdminisrationsSelect2(Select2SearchView):
    model = Administrations
    search_fields = ["LibelleFr","AbreviationFr","code"]
    id_field = "pk"
    text_template = "{code} - {LibelleFr}"
    extra_fields = []
    order_by = "LibelleFr"

class StructuresSelect2(Select2SearchView):
    model = Structures
    search_fields = ["LibelleFr","CodeFr"]
    id_field = "pk"
    text_template = "{LibelleFr}"
    extra_fields = []
    order_by = "LibelleFr"

class BailleursSelect2(Select2SearchView):
    model = Bailleurs
    search_fields = ["Nom_prenom","Raison_social","NIU","Maticule","Nom_Prenom_Representant"]
    id_field = "pk"
    text_template = "{Nom_prenom} {Raison_social}"
    extra_fields = []
    order_by = "Nom_prenom"

class ExercicesSelect2(Select2SearchView):
    model = Exercice
    search_fields = ["annee", "LibelleFR"]
    id_field = "pk"
    text_template = "Exercice budgetaire {annee}"
    extra_fields = ["annee"]
    order_by = "-annee"
    show_all_when_empty = True

class BanquesSelect2(Select2SearchView):
    model = Banques
    search_fields = ["codeBanque","sigle","denominationFR","denominationUS","denominationES","siege","adresse","telephone","fax","email"]
    id_field = "pk"
    text_template = "{codeBanque} - {sigle}"
    extra_fields = []
    order_by = "sigle"

class ImmeublesSelect2(Select2SearchView):
    model = Immeubles
    search_fields = ["Designation"]
    id_field = "pk"
    text_template = "{Designation}"
    extra_fields = []
    order_by = "Designation"
