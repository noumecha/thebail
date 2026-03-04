from django.http import JsonResponse
from django.template.loader import render_to_string
from .views_base import GenericPartialFormView
from ..models import ElementDeDescription, Pieces
from ..forms import *

# partial form views
class RevetementExtPartialFormView(GenericPartialFormView):
    form_class = RevetementExtsForm
    success_message = 'Revetement extérieur enregistré avec succès'

class RevetementIntPartialFormView(GenericPartialFormView):
    form_class = RevetementIntsForm
    success_message = 'Revetement intérieur enregistré avec succès'

class ExercicePartialFormView(GenericPartialFormView):
    form_class = ExercicesForm
    success_message = 'Exercice enregistré avec succès'

class ElementPartialFormView(GenericPartialFormView):
    form_class = ElementDeDescriptionForm
    success_message = 'Élément enregistré avec succès'

    def get_success_html(self, instance, request):
        """Return the HTML row for the new element."""
        form_parent = ImmeublesForm()
        statut_oui = form_parent[f"element_{instance.pk}_statut_oui"]
        statut_non = form_parent[f"element_{instance.pk}_statut_non"]

        html_row = render_to_string(
            "baux/widgets/immeuble_element_row.html",
            {
                "el": {
                    "id": instance.pk,
                    "libelle": instance.libelle,
                    "statut_oui": statut_oui,
                    "statut_non": statut_non,
                }
            },
            request=request,
        )
        return html_row

class PiecePartialFormView(GenericPartialFormView):
    form_class = PiecesForm
    success_message = 'Pièce enregistrée avec succès'

    def get_success_html(self, instance, request):
        """Return the HTML row for the new piece."""
        form_parent = CollectesForm()
        statut_input = form_parent[f"piece_{instance.pk}_statut_oui"]
        nombre_input = form_parent[f"piece_{instance.pk}_nombre"]

        return render_to_string(
            "baux/widgets/piece_element_row.html",
            {
                "el": {
                    "id": instance.pk,
                    "libelle": instance.libelle,
                    "statut_input": statut_input,
                    "nombre_input": nombre_input,
                }
            },
            request=request,
        )

class TypeContratPartialFormView(GenericPartialFormView):
    form_class = TypeContratsForm
    success_message = 'Type de contrat enregistré avec succès'

class BailleursPartialFormView(GenericPartialFormView):
    form_class = BailleursForm
    success_message = 'Bailleur enregistré avec succès'

class ImmeublePartialFormView(GenericPartialFormView):
    form_class = ImmeublesForm
    success_message = 'Immeuble enregistré avec succès'
    template_name = 'baux/partials/immeuble_modal_form.html'
