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
            # informations du contrat et sur le collecteur
            "Numero_fiche_de_collecte",
            "Agent_de_collecte",
            #"Matricule_agent_de_collecte",
            "Date_de_collecte",
            "TypeContrat",
            # informations contrat initial
            "Numero_contrat",
            "Date_signature_contrat",
            "Fonction_signataire_contrat",
            "Date_effet_contrat",
            "Regime_fiscal_contrat",
            "Montant_loyer_mensuel",
            "Devise",
            "RIB_contrat_initial",
            "Fichier_contrat_initial",
            # Bailleur
            "Bailleur",
            # Agent
            "Agent",
            # avenant informations
            "Existance_avenant",
            "Existance_visa_budgetaire",
            "observation",
            "Periodicite_Reglement",
        )
        labels = {
            # informations du contrat et sur le collecteur
            "Numero_fiche_de_collecte" : "Fiche de collecte N°",
            "Agent_de_collecte" : "Agent de collecte",
            #"Matricule_agent_de_collecte" : "Matricule de l'agent de collecte",
            "Date_de_collecte" : "Date de collecte",
            "TypeContrat" : "Typologie du contrat",
            # informations contrat initial
            "Numero_contrat" : "Référence ou Numéro du contrat",
            "Date_signature_contrat" : "Date de signature",
            "Fonction_signataire_contrat" : "Qualité ou fonction du signataire du contrat",
            "Date_effet_contrat" : "Date de prise d'effet",
            "Regime_fiscal_contrat" : "Régime fiscal",
            "Montant_loyer_mensuel" : "Montant du loyer mensuel(TTC)",
            "Devise" : "Devise",
            "RIB_contrat_initial" : "RIB Contrat Initial",
            "Fichier_contrat_initial" : "Fichier Contrat Initial",
            # Bailleur
            "Bailleur" : "Bailleur",
            # Agent
            "Agent" : "Matricule de l'agent de collecte",
            # avenant informations
            #"Existance_avenant" : "Existance d'au moins un avenant ?",
            #"Existance_visa_budgetaire" : "Existance d'un visa budgétaire ?",
            "observation" : "Observation générale",
            "Periodicite_Reglement" : "Périodicité de règlement selon le contrat",
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
        # remove labels :
        self.fields['Existance_avenant'].label = ""
        self.fields['Existance_visa_budgetaire'].label = ""
        # Si l'instance a déjà une valeur (form update)
        if self.instance.pk:
            if self.instance.Bailleur:
                self.fields['Bailleur'].queryset = Bailleurs.objects.filter(
                    pk=self.instance.Bailleur.pk
                )
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
                Column(
                    HTML("""
                        <hr>
                    """),
                    css_class='overflow-hidden form-group col-md-12'
                ),
            ),
            Row(
                Column(css_class='text-center overflow-hidden form-group col-md-3 mb-0'),
                Column(
                    HTML("""
                        <h3 class="p-0">Fiche de Collecte N°</h3>
                    """),
                    css_class='overflow-hidden form-group col-md-3 p-0 m-0'
                ),
                Column(FloatingField("Numero_fiche_de_collecte"), css_class='text-center overflow-hidden form-group col-md-3 mb-0'),
                Column(css_class='text-center overflow-hidden form-group col-md-3 mb-0'),
            ),
            Row(
                Column(
                    HTML("""
                        <label for="id_Agent">Selectionner le matricule d'un Agent</label>
                        <div class="d-flex align-items-center">
                            {{ form.Agent }}
                        </div>
                    """),
                    css_class='overflow-hidden form-group col-md-4 mb-3'
                ),
                Column(FloatingField("Agent_de_collecte", css_class="disabled"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                Column(FloatingField("Date_de_collecte"), css_class='overflow-hidden form-group col-md-4 mb-0'),
            ),
            # informations sur le contrat
            Row(
                Column(
                    HTML("<h4 class='bg-gray text-white p-2 mt-2 mb-2'>SECTION 1. INFORMATIONS CONTRACTUELLES</h4>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>I. Typologie du contrat</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    HTML("""
                        <label for="id_TypeContrat">Selectionner un type de contrat</label>
                        <div class="d-flex align-items-center">
                            {{ form.TypeContrat }}
                            <button type="button" id="id-add-contrat-type" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addTypeContratModal">
                                + Ajouter
                            </button>
                        </div>
                    """),
                    css_class='overflow-hidden form-group col-md-12 mb-3'
                ),
                css_class="form-row"
            ),
            # Element juridiques section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>II. Elements juridiques</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                # title of subsection
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>a- Contrat Initial</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                # content
                Fieldset(
                    "Contrat Initial",
                    Row(
                        Column(
                            FloatingField("Numero_contrat"), css_class='overflow-hidden form-group col-md-3 mb-0'
                        ),
                        Column(
                            FloatingField("Date_signature_contrat"), css_class='overflow-hidden form-group col-md-3 mb-0'
                        ),
                        Column(FloatingField("Fonction_signataire_contrat"), css_class='overflow-hidden overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_effet_contrat"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Regime_fiscal_contrat"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Montant_loyer_mensuel"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Devise"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("RIB_contrat_initial"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Fichier_contrat_initial"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        css_class="form-row"
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Existence d'avenant / visa budgétaire",
                    Row(
                        Column(css_class='text-center overflow-hidden form-group col-md-1 mb-0'),
                        Column(
                            HTML("""
                                <h6 class="p-0 m-0" for="id_Existance_avenant">Existence d'au moins un avenant ?</h6>
                            """),
                            InlineRadios("Existance_avenant", css_class="p-0 m-0"),
                            css_class='overflow-hidden text-center p-2 bg-white form-group col-md-4 mb-0'
                        ),
                        Column(css_class='text-center overflow-hidden form-group col-md-2 mb-0'),
                        Column(
                            HTML("""
                                <h6 class="p-0 m-0" for="id_Existance_visa_budgetaire">Existence du visa budgétaire ?</h6>
                            """),
                            InlineRadios("Existance_visa_budgetaire", css_class="p-0 m-0"),
                            css_class='overflow-hidden text-center p-2 bg-white form-group col-md-4 mb-0'
                        ),
                        Column(css_class='text-center overflow-hidden form-group col-md-1 mb-0'),
                        Column(
                            HTML("<h5 class='text-bold fw bg-secondary-subtle mt-2' id='avenant-collecte-form-title'>b- Avenants liés au Contrat Initial</h5>"),
                            css_class='overflow-hidden form-group col-md-12 mb-0'
                        ),
                        Formset("avenants_formset"),
                        Column(
                            HTML("""
                                <div id="avenant-collecte-list"></div>
                            """)
                        ),
                        css_class="form-row"
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                Column(
                    HTML("<h5 class='mt-2 text-bold fw bg-secondary-subtle'>c- Périodicité de règlement selon le contrat</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                Column(FloatingField("Periodicite_Reglement"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                # Bailleur section
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>III. bailleur</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                Column(
                    HTML("""
                        <label for="id_Bailleur">Selectionner un Bailleur</label>
                        <div class="d-flex align-items-center">
                            {{ form.Bailleur }}
                            <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addBailleurModal">
                                + Ajouter
                            </button>
                        </div>
                    """),
                    css_class='overflow-hidden form-group col-md-12 mb-3'
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>c- Ayants Droits du Bailleurs</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                Formset("ayants_droits_formset"),
                Column(
                    HTML("""
                        <hr>
                        <table id="ayantdroit-collecte-table" class='table bg-white table-bordered mt-2'>
                            <thead class='thead-dark'>
                                <tr>
                                    <th>
                                        Noms & Prénoms
                                    </th>
                                    <th>
                                        Contact
                                    </th>
                                    <th>
                                        Reference Grosse
                                    </th>
                                    <th>
                                        Date de prise d'effet de Grosse
                                    </th>
                                    <th>
                                        Reference Certificat de non appel
                                    </th>
                                    <th>
                                        Date de prise d'effet du certificat
                                    </th>
                                    <th>
                                        Action
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr id='empty-ayantdroit-row'>
                                    <td colspan="7">Aucun ayant droit du bailleur ajouté ...</td>
                                </tr>
                            </tbody>
                        </table>
                    """),
                ),
                css_class="p-3 pt-0"
            ),
            # Non-Mandatement section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>IV. attestion de non-mandatement (non-encore payé)</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Formset("non_mandatements_formset"),
                Column(
                    HTML("""
                        <button type="button"
                            class="btn btn-outline-primary add-form"
                            id="nonmandatement-collecte-add-btn"
                            data-formset="non_mandatements"
                            data-table="nonmandatement-collecte-table"> + Ajouter à la liste </button>
                    """
                    ),
                    css_class='overflow-hidden form-group col-md-3 mb-0'
                ),
                Column(
                    HTML("""
                        <hr>
                        <table id="nonmandatement-collecte-table" class='table-responsive bg-white table table-bordered mt-2'>
                            <thead class='thead-dark'>
                                <tr>
                                    <th rowspan="2">
                                        Exercice
                                    </th>
                                    <th rowspan="2">
                                        Loyer Mensuel
                                    </th>
                                    <th rowspan="2">
                                        Reference de l'attestation de non mandatement & Date de signature
                                    </th>
                                    <th colspan="12">
                                        Mois non-mandatatés
                                    </th>
                                    <th rowspan="2">
                                        Montant Total par exercice
                                    </th>
                                    <th rowspan="2">
                                        Visa budgétaire / Signature CF ?
                                    </th>
                                    <th rowspan="2">
                                        Reference Contrat / Avenant
                                    </th>
                                    <th rowspan="2">
                                        Action
                                    </th>
                                </tr>
                                <tr>
                                    <th>
                                        J
                                    </th>
                                    <th>
                                        F
                                    </th>
                                    <th>
                                        M
                                    </th>
                                    <th>
                                        A
                                    </th>
                                    <th>
                                        M
                                    </th>
                                    <th>
                                        J
                                    </th>
                                    <th>
                                        J
                                    </th>
                                    <th>
                                        A
                                    </th>
                                    <th>
                                        S
                                    </th>
                                    <th>
                                        O
                                    </th>
                                    <th>
                                        N
                                    </th>
                                    <th>
                                        D
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr id='empty-ayantdroit-row'>
                                    <td colspan="30">Aucune attestation de non mandatement ajouter ...</td>
                                </tr>
                            </tbody>
                        </table>
                    """),
                ),
                css_class="p-3 pt-0"
            ),
            # Immeuble Section
            Row(
                Column(
                    HTML("<h4 class='bg-gray text-white p-2 mt-2 mb-2'>SECTION 2. INFORMATIONS SUR L'IMMEUBLE</h4>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                HTML("{% for form in immeubles_formset.forms %}{{ form.render_collecte_layout|safe }}{% endfor %}"),
                #Formset("immeubles_formset"),
                css_class="p-3 pt-0"
            ),
            Row(
                Formset("occupants_residence_formset"),
                css_class="p-3 pt-0"
            ),
            Row(
                Formset("occupants_bureau_formset"),
                css_class="p-3 pt-0"
            ),
            # Pièces collectées
            Row(
                Column(
                    HTML("<h4 class='text-uppercase bg-gray text-white p-2 mt-2 mb-2'>SECTION 3. pièces collectées</h4>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Pieces Collectées",
                    HTML(html_content),
                    HTML("""
                    <div class="d-flex align-items-center">
                        <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addPieceModal">
                            Ajouter une pièce
                        </button>
                    </div>"""),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(FloatingField("observation"), css_class='overflow-hidden form-group mt-1 col-md-12 mb-0'),
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
