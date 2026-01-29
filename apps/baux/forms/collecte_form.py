from django import forms
from ..models import *
from .utils import MultipleFileField
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, HTML
from dal import autocomplete
from .forms import *

# collectes form
class CollectesForm(forms.ModelForm):
    class Meta:
        model = Collectes

        fields = (
            "Numero_fiche_de_collecte",
            "Date_de_collecte",
            "observation_generale",
            "signature_responsable",
            "pieces",
            "Contrat",
            "Immeuble",
            "Agent"
        )
        labels = {
            "Numero_fiche_de_collecte" : "Numéro de la fiche de collecte",
            "Date_de_collecte" : "Date de collecte",
            "observation_generale" : "Observation générale",
            "signature_responsable" : "Signature du responsable",
            "pieces" : "pieces",
            "Contrat" : "Contrat",
            "Immeuble" : "Immeuble",
            "Agent" : "Responsable de collecte",
        }
        widgets = {
            'Date_de_collecte' : forms.TextInput(attrs={'type': 'date'}),
            'Date_signature_contrat' : forms.TextInput(attrs={'type': 'date'}),
            'Date_effet_contrat' : forms.TextInput(attrs={'type': 'date'}),
            'Existance_avenant': forms.RadioSelect,
            'Existance_visa_budgetaire': forms.RadioSelect,
            'Bailleur': autocomplete.ModelSelect2(url='baux:bailleur_autocomplete'),
            'Agent': autocomplete.ModelSelect2(url='baux:agent_autocomplete'),
        }


    def __init__(self, *args, **kwargs):
        super(CollectesForm, self).__init__(*args, **kwargs)
        # on POST
        if 'Bailleur' in self.data:
            try:
                bailleur_id = int(self.data.get('Bailleur'))
                self.fields['Bailleur'].queryset = Bailleurs.objects.filter(pk=bailleur_id)
            except (ValueError, TypeError):
                pass
        if 'Agent' in self.data:
            try:
                agent_id = int(self.data.get('Agent'))
                self.fields['Agent'].queryset = AgentCollecte.objects.filter(pk=agent_id)
            except (ValueError, TypeError):
                pass
        #
        pieces = list(Pieces.objects.all())
        piece_groups = []
        group = []

        for index, el in enumerate(pieces, start=1):
            statut_name = f"piece_{el.pk}_statut_oui"
            nombre_name = f"piece_{el.pk}_nombre"
            images_name = f"piece_{el.pk}_images"

            self.fields[statut_name] = forms.BooleanField(
                required=False,
                label=el.libelle,
                widget=forms.CheckboxInput(attrs={"class": "form-check-input statut-checkbox", "data-group": f"element_{el.pk}"}),
            )
            self.fields[nombre_name] = forms.IntegerField(
                required=False, min_value=0, initial=0, label="",
            )
            self.fields[images_name] = MultipleFileField(
                required=False,
                label="",
            )

            # Optional: set initial values when editing an existing Collecte
            if self.instance and self.instance.pk:
                try:
                    link = PieceCollectes.objects.get(collecte=self.instance, piece=el)
                    self.fields[statut_name].initial = link.statut
                    self.fields[nombre_name].initial = link.nombre
                    self.fields[images_name].initial = link.images
                except PieceCollectes.DoesNotExist:
                    pass

            group.append({
                "id": el.pk,
                "libelle": el.libelle,
                "statut_input": self[statut_name],
                "nombre_input": self[nombre_name],
                "images_input": self[images_name],
            })

            if index % 9 == 0 or index == len(pieces):
                piece_groups.append(group)
                group = []

        html_content = render_to_string("baux/widgets/pieces_template.html", {"piece_groups": piece_groups})
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            # title informations :
            Row(
                Fieldset(
                    "Pieces Collectées",
                    HTML(html_content),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(FloatingField("observation_generale"), css_class='overflow-hidden form-group mt-1 col-md-12 mb-0'),
                css_class='p-3 pt-2 form-row'
            ),
            Column(
                Submit(
                    "save",
                    "Enregistrer",
                    css_class="btn btn-lg btn-outline-primary"
                ),
                css_class='overflow-hidden form-group col-md-6 col-lg-6 mb-0'
            ),
        )
        self.helper.form_tag = False
