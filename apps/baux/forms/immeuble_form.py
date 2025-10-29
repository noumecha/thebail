from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, Field, HTML
from .nonmandatement_form import *
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

# immeubles form
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

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
            statut = self.cleaned_data.get(f"element_{element.id}_statut")
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
        # Dynamically create fields for each element
        elements = list(ElementDeDescription.objects.all())
        # manage select 2 input 
        if 'arrondissement' in self.data:
            try:
                arrondissement_id = int(self.data.get('arrondissement'))
                self.fields['arrondissement'].queryset = Arrondissemements.objects.filter(pk=arrondissement_id)
            except (ValueError, TypeError):
                pass
        # 1) Create dynamic fields
        for el in elements:
            self.fields[f"element_{el.pk}_statut"] = forms.BooleanField(
                required=False, label=el.libelle
            )
            self.fields[f"element_{el.pk}_nombre"] = forms.IntegerField(
                required=False, min_value=0, initial=0, label="",
            )
            # Optional: set initial values when editing an existing Immeuble
            if self.instance and self.instance.pk:
                try:
                    link = ImmeubleElement.objects.get(immeuble=self.instance, element=el)
                    self.fields[f"element_{el.pk}_statut"].initial = link.statut
                    self.fields[f"element_{el.pk}_nombre"].initial = link.nombre
                except ImmeubleElement.DoesNotExist:
                    pass
        # 2) Build the dynamic rows for the layout
        element_rows = []
        for el in elements:
            element_rows.append(
                Column(
                    Field(f"element_{el.pk}_statut", css_class=""),
                    Field(f"element_{el.pk}_nombre", css_class="ms-2 w-50"),
                    css_class="m-0 col-md-3 d-flex align-items-center justify-content-center"
                )
            )
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
                        #Column(FloatingField("Revetement_interieure"), css_class='overflow-hidden form-group col-md-6 mb-0'),
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
                        #Column(FloatingField("Revetement_exterieure"), css_class='overflow-hidden form-group col-md-6 mb-0'),
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
                    Row(
                        *element_rows,
                        css_class="form-row"
                    ),
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
            #Row(
            #    Fieldset(
            #        "Occupants Pour résidence",
            #        Formset("occupants_residence_formset"),
            #        css_class="bg-white line__text border p-2 pt-4"
            #    )
            #),
            #Row(
            #    Fieldset(
            #        "Occupants Pour bureaux",
            #        Formset("occupants_bureau_formset"),
            #        css_class="bg-white line__text border p-2 pt-4"
            #    )
            #)
        )     
        self.fields['Date_Construction'].required = False;   