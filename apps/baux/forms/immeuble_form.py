from django import forms
from ..models import *
from .utils import MultipleFileField
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Field, HTML
from .nonmandatement_form import *
from django.template.loader import render_to_string
from dal import autocomplete
from .ayantdroit_form import *

# immeuble element formset
class ImmeubleElementForm(forms.ModelForm):
    class Meta:
        model = ImmeubleElement
        fields = ("element", "nombre", "statut")
        labels = {
            "element": "Elément",
            "nombre": "Nombre",
            "statut": "Statut (coché pour activé)",
        }
        widgets = {
            'statut' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        def __init__(self, *args, **kwargs):
            super(ImmeubleElementForm, self).__init__(*args, **kwargs)
            self.helper =  FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column(FloatingField("statut"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    Column(FloatingField("element"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                    Column(FloatingField("nombre"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),

            )

class ImmeublesForm(forms.ModelForm):
    images = MultipleFileField()

    class Meta:
        model = Immeubles

        fields = (
            # idenfification fields
            "Designation","Construction","Date_Construction","Type_location","Nombre_de_pieces", "Norme","Superficie_louer",
            # localisation fields
            "Type_localisation","pays","Ville","Rue","region","departement","arrondissement","Quartier","Coordonee_gps",
            # etat physique du batiement fields
            "Situation_de_la_batisse","Revetement_interieure","Revetement_exterieure", "observation","images"
        )
        labels = {
            # idenfification labels
            "Designation": " Désignation du Bien",
            "Construction" : "Type de construction",
            "Date_Construction" : "Date de construction",
            "Nombre_de_pieces" : "Nombre total de pièces",
            "Superficie_louer" : "Superficie louée(m²)",
            "Norme" : "Norme de Cadastrale",
            "Type_location" : "Type de location",
            # etat physique du batiement fields
            "Revetement_interieure" : "Revetement interieur",
            "Revetement_exterieure" : "Revetement exterieur",
            "observation" : "Observation",
            "Situation_de_la_batisse" : "Etat de la batisse",
            # localisation labels
            "Type_localisation" : "Type de localisation",
            "pays" : "Pays",
            "Ville" : "Ville",
            "Rue" : "Rue",
            "region" : "Région",
            "departement" : "Département",
            "arrondissement" : "Arrondissement",
            "Quartier" : "Quartier",
            "Coordonee_gps" : "Coordonnées GPS",
            "images" : "Chargés les images de l'immeuble"
        }
        widgets = {
            'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
            'arrondissement': autocomplete.ModelSelect2(url='baux:arrondissement_autocomplete'),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)

        # after saving the immeuble, create/update ImmeubleElement
        for element in ElementDeDescription.objects.all():
            #statut = self.cleaned_data.get(f"element_{element.id}_statut")
            statut = self.cleaned_data.get(f"element_{element.pk}_statut")
            if statut in ["True", "true", True]:
                statut = True
            else:
                statut = False
            nombre = self.cleaned_data.get(f"element_{element.id}_nombre")

            if statut:  # if element is selected
                obj, created = ImmeubleElement.objects.update_or_create(
                    immeuble=instance, element=element,
                    defaults={"statut": statut, "nombre": nombre or 0}
                )
            else:
                # If unchecked, delete existing link if it exists
                ImmeubleElement.objects.filter(immeuble=instance, element=element).delete()

        return instance

    def partial_form(self):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_tag = False # remove form tags in the modal
        helper.disable_csrf = True # we use default csrf token in the template
        helper.layout = Layout(
            Row(
                Fieldset(
                        "I. Identification",
                        Row(
                            Column(FloatingField("Designation"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                            Column(FloatingField("Construction"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                            Column(FloatingField("Date_Construction"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                            Column(FloatingField("Nombre_de_pieces"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                            Column(FloatingField("Superficie_louer"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                            Column(FloatingField("Norme"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                            Column(FloatingField("Type_location"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                            #Column(FloatingField("Type_construction"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                            css_class='form-row'
                        ),
                        css_class="bg-white line__text border p-2 pt-4"
                    ),
                    css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "II. Localisation",
                    Row(
                        #Column(FloatingField("Localisation"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        Column(FloatingField("Type_localisation"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("pays"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Ville"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Rue"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("region"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("departement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Quartier"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "III. Etat physique du batiment",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        Column(FloatingField("Revetement_interieure"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Revetement_exterieure"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("observation"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "IV. Description de la batisse",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            """Row(
                Fieldset(
                    "Occupants Pour résidence",
                    Formset(OccupantsFormSet("occupants_formset")),
                    css_class="bg-white line__text border p-2 pt-4"
                )
            ),
            Row(
                Fieldset(
                    "Occupants Pour bureaux",
                    Formset("occupants_bureau_formset"),
                    css_class="bg-white line__text border p-2 pt-4"
                )
            )"""
        )
        return helper

    def __init__(self, *args, **kwargs):
        super(ImmeublesForm, self).__init__(*args, **kwargs)
        # manage select 2 input
        if 'arrondissement' in self.data:
            try:
                arrondissement_id = int(self.data.get('arrondissement'))
                self.fields['arrondissement'].queryset = Arrondissemements.objects.filter(pk=arrondissement_id)
            except (ValueError, TypeError):
                pass
        # immeuble elements
        elements = list(ElementDeDescription.objects.all())
        element_groups = []
        group = []

        for index, el in enumerate(elements, start=1):
            statut_oui_name = f"element_{el.pk}_statut_oui"
            statut_non_name = f"element_{el.pk}_statut_non"
            nombre_name = f"element_{el.pk}_nombre"

            # ✅ Deux checkboxes
            self.fields[statut_oui_name] = forms.BooleanField(
                required=False,
                label="Oui",
                widget=forms.CheckboxInput(attrs={"class": "form-check-input statut-checkbox", "data-group": f"element_{el.pk}"}),
            )
            self.fields[statut_non_name] = forms.BooleanField(
                required=False,
                label="Non",
                widget=forms.CheckboxInput(attrs={"class": "form-check-input statut-checkbox", "data-group": f"element_{el.pk}"}),
            )
            self.fields[nombre_name] = forms.IntegerField(
                required=False, min_value=0, initial=0, label="", widget=forms.NumberInput(attrs={"class": "form-control"}),
            )

            # Valeurs initiales (si instance)
            if self.instance and self.instance.pk:
                try:
                    link = ImmeubleElement.objects.get(immeuble=self.instance, element=el)
                    if link.statut is True:
                        self.fields[statut_oui_name].initial = True
                    elif link.statut is False:
                        self.fields[statut_non_name].initial = True
                    self.fields[nombre_name].initial = link.nombre
                except ImmeubleElement.DoesNotExist:
                    pass

            group.append({
                "id": el.pk,
                "libelle": el.libelle,
                "statut_oui": self[statut_oui_name],
                "statut_non": self[statut_non_name],
                "nombre_input": self[nombre_name],
            })

            if index % 9 == 0 or index == len(elements):
                element_groups.append(group)
                group = []
        self.element_groups = element_groups
        # render dynamic HTML content for elements
        html_content = render_to_string("baux/widgets/immeuble_elements.html", {"element_groups": element_groups})
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>I. Identification</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Designation"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Construction"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_Construction"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Nombre_de_pieces"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Superficie_louer"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Norme"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Type_location"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("images"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>II. Localisation</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Localisation",
                    Row(
                        Column(FloatingField("Type_localisation"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("pays"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Ville"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Rue"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("region"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("departement"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Quartier"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Coordonee_gps"), css_class='overflow-hidden form-group col-md-9 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>III. Etat physique du batiment</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row (
                Fieldset(
                    "Etat physique du batiment",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(
                            HTML("""
                                <div class="d-flex align-items-center">
                                    {{ form.Revetement_interieure }}
                                    <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addRevetementInterieureModal">
                                        +
                                    </button>
                                </div>
                            """),
                            css_class='overflow-hidden form-group col-md-4 mb-3'
                        ),
                        Column(
                            HTML("""
                                <div class="d-flex align-items-center">
                                    {{ form.Revetement_exterieure }}
                                    <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addRevetementExterieureModal">
                                        +
                                    </button>
                                </div>
                            """),
                            css_class='overflow-hidden form-group col-md-4 mb-3'
                        ),
                        Column(FloatingField("observation"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # Dynamic section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>IV. Description de la batisse</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Description de la batisse",
                    HTML(html_content),
                    HTML("""
                    <div class="d-flex align-items-center">
                        <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addElementModal">
                            Ajouter un élément
                        </button>
                    </div>"""),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # Occupant section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>V. Occupants actuels de l'immeuble </h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
        )
        self.fields['Date_Construction'].required = False

    def render_collecte_layout(self):
        """Render the full layout from the external template."""
        # manage fields
        self.fields["Designation"].label = ""
        self.fields["Coordonee_gps"].label = ""
        #
        for name, field in self.fields.items():
            widget = field.widget
            if not widget.attrs.get("class"):
                if isinstance(widget, forms.Select):
                    widget.attrs["class"] = "form-select"
                else:
                    widget.attrs["class"] = "form-control"

        # type constructions :
        if "Construction" in self.fields:
            del self.fields["Construction"]
        self.construction_choices = TypeConstructions.objects.all()
        self.fields["construction_choice"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )
        # type de locations :
        if "Type_location" in self.fields:
            del self.fields["Type_location"]
        self.type_locations = TypeLocations.objects.all()
        self.fields["type_location_choice"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )
        # statutbatisse :
        if "Situation_de_la_batisse" in self.fields:
            del self.fields["Situation_de_la_batisse"]
        self.statut_batisses = StatutBatisse.objects.all()
        self.fields["statut_batisse_choice"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )
        # revetement interieure
        if "Revetement_interieure" in self.fields:
            del self.fields["Revetement_interieure"]
        self.revetement_interieures = RevetementInts.objects.all()
        self.fields["revetement_interieure_choice"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )
        # revetement extérieure
        if "Revetement_exterieure" in self.fields:
            del self.fields["Revetement_exterieure"]
        self.revetement_exterieures = RevetementExts.objects.all()
        self.fields["revetement_exterieure_choice"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput()
        )

        return render_to_string(
            "baux/forms/immeuble_form_layout.html",
            {
                "form": self,
                "element_groups": self.element_groups,
                "type_constructions" : self.construction_choices,
                "type_locations" : self.type_locations,
                "statut_batisses" : self.statut_batisses,
                "revetement_interieures" : self.revetement_interieures,
                "revetement_exterieures" : self.revetement_exterieures,
                "occupants_residence_formset" : self.occupants_residence_formset,
                "occupants_bureau_formset" : self.occupants_bureau_formset,
            },
        )

    def clean(self):
        cleaned = super().clean()
        selected_label = cleaned.get("construction_choice")
        if not selected_label:
            raise forms.ValidationError("Veuillez choisir un type de construction.")

        type_obj, _ = TypeConstructions.objects.get_or_create(libelle=selected_label)
        cleaned["Construction"] = type_obj
        return cleaned
