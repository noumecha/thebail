from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML

# non-mandatement forms
class NonMandatementForm(forms.ModelForm):
    class Meta:
        model = Non_Mandatement
        fields = (
            "Exercice","Loyer_Mensuel","Ref_Attestattion","janvier","fevrier","mars","avril",
            "mai","juin","juillet","aout","septembre","octobre","novembre","decembre","Montant_total_exercice",
            "Visa_budgétaire","Ref_contrat_avenant",#"Etat","Date_signature",
        )
        labels = {
            "Exercice" : "Exercice",
            "Loyer_Mensuel" : "Loyer Mensuel",
            "Ref_Attestattion" : "Référence de l'attestation de non mandatement",
            #"Date_signature" : "Date de signature",
            "janvier" : "J",
            "fevrier" : "F",
            "mars" : "M",
            "avril" : "A",
            "mai" : "M",
            "juin" : "J",
            "juillet" : "J",
            "aout" : "A",
            "septembre" : "S",
            "octobre" : "O",
            "novembre" : "N",
            "decembre" : "D",
            "Montant_total_exercice" : "Montant total par exercice (Nbre de mois x Loyer Mensuel)",
            #"Visa_budgétaire" : "Visa budgétaire / Signature CF ?",
            "Ref_contrat_avenant" : "Reference Contrat / Avenant",
            #"Etat" : "Etat",
        }
        widgets = {
            "Date_signature"  :  forms.TextInput(attrs={'type': 'date'}),
            'Visa_budgétaire': forms.RadioSelect,
        }
    def __init__(self, *args, **kwargs):
        super(NonMandatementForm, self).__init__(*args, **kwargs)
        # remove labels : 
        self.fields['Visa_budgétaire'].label = ""
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations Générales",
                    Row(
                        #Column(FloatingField("Exercice"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(
                            HTML("""
                                <div class="d-flex align-items-center">
                                    {{ form.Exercice }}
                                    <button type="button" class="btn btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addExerciceModal">
                                        +
                                    </button>
                                </div>
                            """),
                            css_class='overflow-hidden form-group col-md-4 mb-3'
                        ),
                        Column(FloatingField("Loyer_Mensuel"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Ref_Attestattion"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        #Column(FloatingField("Date_signature"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        #Column(FloatingField("Etat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Mois non-mandatés",
                    Row(
                        Column("janvier", css_class="col-md-1"),
                        Column("fevrier", css_class="col-md-1"),
                        Column("mars", css_class="col-md-1"),
                        Column("avril", css_class="col-md-1"),
                        Column("mai", css_class="col-md-1"),
                        Column("juin", css_class="col-md-1"),
                        Column("juillet", css_class="col-md-1"),
                        Column("aout", css_class="col-md-1"),
                        Column("septembre", css_class="col-md-1"),
                        Column("octobre", css_class="col-md-1"),
                        Column("novembre", css_class="col-md-1"),
                        Column("decembre", css_class="col-md-1"),
                        css_class="form-row"
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Validation",
                    Row(
                        Column(FloatingField("Montant_total_exercice"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(
                            HTML("""
                                <h6 class="p-0 m-0" for="id_Visa_budgétaire">Visa budgétaire / Signature CF ?</h6>
                            """),
                            InlineRadios("Visa_budgétaire", css_class="p-0 m-0"),
                            css_class='overflow-hidden text-center p-2 bg-white form-group col-md-4 mb-0'
                        ),
                        Column(FloatingField("Ref_contrat_avenant"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
        )