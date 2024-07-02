from django import forms
from .models import BudgetArticleMvtDepense, BudgetArticle, BudgetArticleMvtRecette, BudgetExecution

class ControleCompteGestionForm(forms.ModelForm):
    class Meta:
        model = BudgetExecution

        fields = ('cg_rr_bud_primitif', 'cg_rr_ae_speciale', 'cg_rr_emission', 'cg_rr_recouvrement', 'cg_rr_anv', 'cg_rr_r', 'cg_rr_d', 'cg_rr_ir', 'cg_dd_bud_primitif', 'cg_dd_ae_speciale', 'cg_dd_virement_credits', 'cg_dd_montant_pris_en_charge', 'cg_dd_reglement')
        labels = {
            "cg_rr_bud_primitif": "Budget Primitif en recette",
            "cg_rr_ae_speciale": "Autorisation spéciale en recette",
            "cg_rr_emission": "Recettes émises",
            "cg_rr_recouvrement": "Recouvrement effectif",
            "cg_rr_anv": "Admission en non valeur",
            "cg_rr_r": "Restes à recouvrer recouvrables",
            "cg_rr_d": "Restes à recouvrer douteux",
            "cg_rr_ir": "Restes à recouvrer irrecouvrables",
            
            "cg_dd_bud_primitif": "Budget Primitif en depense",
            "cg_dd_ae_speciale": "Autorisation speciale en depense",
            "cg_dd_virement_credits": "Virements de crédits",
            "cg_dd_montant_pris_en_charge": "Montant pris en charge",
            "cg_dd_reglement": "Règlement",
        }
    def __init__(self, *args, **kwargs):
        super(ControleCompteGestionForm, self).__init__(*args, **kwargs)

class ControleCompteAdmForm(forms.ModelForm):
    class Meta:
        model = BudgetExecution

        fields = ('ca_rr_bud_primitif', 'ca_rr_ae_speciale', 'ca_dd_virement_credits', 'ca_rr_emission', 'ca_rr_recouvrement', 'ca_rr_anv', 'ca_rr_r', 'ca_rr_d', 'ca_rr_ir', 'ca_dd_bud_primitif', 'ca_dd_ae_speciale', 'ca_dd_droit_constate', 'ca_dd_somme_payee', 'ca_dd_rap', 'ca_dd_denl', 'ca_dd_cp_annule', 'ca_dd_cp_invest_report')

        labels = {
            "ca_rr_bud_primitif": "Budget Primitif en recette",
            "ca_rr_ae_speciale": "Autorisation spéciale en recette",
            "ca_rr_emission": "Recettes émises",
            "ca_rr_recouvrement": "Recouvrement effectif",
            "ca_rr_anv": "Admission en non valeur",
            "ca_rr_r": "Restes à recouvrer recouvrables",
            "ca_rr_d": "Restes à recouvrer douteux",
            "ca_rr_ir": "Restes à recouvrer irrecouvrables",

            "ca_dd_bud_primitif": "Budget Primitif en depense",
            "ca_dd_ae_speciale": "Autorisation spéciale en depense",
            "ca_dd_virement_credits": "Virements de crédits",
            "ca_dd_droit_constate": "Droits constatés",
            "ca_dd_somme_payee": "Sommes Payées",
            "ca_dd_rap": "Restes à payer",
            "ca_dd_denl": "Dépenses engagées non liquidées",
            "ca_dd_cp_annule": "Crédits annulés faute d'emploi",
            "ca_dd_cp_invest_report": "Crédits d'investissement à reporter",
            }
    def __init__(self, *args, **kwargs):
        super(ControleCompteAdmForm, self).__init__(*args, **kwargs)

class CompteAdmRecetteFormSansArticle(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtRecette
        #fields = '__all__'
        fields = ('ca_bud_primitif', 'ca_auto_speciale', 'ca_emission', 'ca_recouvrement', 'ca_anv', 'ca_rr_r', 'ca_rr_d', 'ca_rr_ir')
        labels = {
            "ca_bud_primitif": "Budget Primitif",
            "ca_auto_speciale": "Autorisation spéciale",
            "ca_emission": "Recettes émises",
            "ca_recouvrement": "Recouvrement effectif",
            "ca_anv": "Admission en non valeur",
            "ca_rr_r": "Restes à recouvrer recouvrables",
            "ca_rr_d": "Restes à recouvrer douteux",
            "ca_rr_ir": "Restes à recouvrer irrecouvrables",
        }
    def __init__(self, *args, **kwargs):
        super(CompteAdmRecetteFormSansArticle, self).__init__(*args, **kwargs)

class CompteGestionRecetteFormSansArticle(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtRecette
        #fields = '__all__'
        fields = ('cg_bud_primitif', 'cg_auto_speciale', 'cg_emission', 'cg_recouvrement', 'cg_anv', 'cg_rr_r', 'cg_rr_d', 'cg_rr_ir')
        labels = {
            "cg_bud_primitif": "Budget Primitif",
            "cg_auto_speciale": "Autorisation spéciale",
            "cg_emission": "Recettes émises",
            "cg_recouvrement": "Recouvrement effectif",
            "cg_anv": "Admission en non valeur",
            "cg_rr_r": "Restes à recouvrer recouvrables",
            "cg_rr_d": "Restes à recouvrer douteux",
            "cg_rr_ir": "Restes à recouvrer irrecouvrables",
        }
    def __init__(self, *args, **kwargs):
        super(CompteGestionRecetteFormSansArticle, self).__init__(*args, **kwargs)

class CompteAdmRecetteForm(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtRecette
        #fields = '__all__'
        fields = ('budget_article', 'ca_bud_primitif', 'ca_auto_speciale', 'ca_emission', 'ca_recouvrement', 'ca_anv', 'ca_rr_r', 'ca_rr_d', 'ca_rr_ir')
        labels = {
            "budget_article": "Compte",
            "ca_bud_primitif": "Budget Primitif",
            "ca_auto_speciale": "Autorisation spéciale",
            "ca_emission": "Recettes émises",
            "ca_recouvrement": "Recouvrement effectif",
            "ca_anv": "Admission en non valeur",
            "ca_rr_r": "Restes à recouvrer recouvrables",
            "ca_rr_d": "Restes à recouvrer douteux",
            "ca_rr_ir": "Restes à recouvrer irrecouvrables",
        }
    def __init__(self, *args, **kwargs):
        super(CompteAdmRecetteForm, self).__init__(*args, **kwargs)
        mouvements = BudgetArticleMvtRecette.objects.all()
        list_article_mv = []
        for m in mouvements:
            list_article_mv.append(m.budget_article.code)
        list_article_mv = []
        self.fields['budget_article'] = forms.ModelChoiceField(queryset=BudgetArticle.objects.filter(type_article='1').exclude(code__in=list_article_mv))


class CompteGestionRecetteForm(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtRecette
        #fields = '__all__'
        fields = ('budget_article', 'cg_bud_primitif', 'cg_auto_speciale', 'cg_emission', 'cg_recouvrement', 'cg_anv', 'cg_rr_r', 'cg_rr_d', 'cg_rr_ir')
        labels = {
            "budget_article": "Compte",
            "cg_bud_primitif": "Budget Primitif",
            "cg_auto_speciale": "Autorisation spéciale",
            "cg_emission": "Recettes émises",
            "cg_recouvrement": "Recouvrement effectif",
            "cg_anv": "Admission en non valeur",
            "cg_rr_r": "Restes à recouvrer recouvrables",
            "cg_rr_d": "Restes à recouvrer douteux",
            "cg_rr_ir": "Restes à recouvrer irrecouvrables",
        }
    def __init__(self, *args, **kwargs):
        super(CompteGestionRecetteForm, self).__init__(*args, **kwargs)
        mouvements = BudgetArticleMvtRecette.objects.all()
        list_article_mv = []
        for m in mouvements:
            list_article_mv.append(m.budget_article.code)
        list_article_mv = []
        self.fields['budget_article'] = forms.ModelChoiceField(queryset=BudgetArticle.objects.filter(type_article='1').exclude(code__in=list_article_mv))



class CompteGestionDepenseFormSansArticle(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtDepense
        #fields = '__all__'
        fields = ('cg_bud_primitif', 'cg_ae_speciale', 'cg_virement_credits', 'cg_montant_pris_en_charge', 'cg_reglement')
        labels = {
            "cg_bud_primitif": "Budget Primitif",
            "cg_ae_speciale": "Autorisation speciale",
            "cg_virement_credits": "Virements de crédits",
            "cg_montant_pris_en_charge": "Montant pris en charge",
            "cg_reglement": "Règlement",
        }
    def __init__(self, *args, **kwargs):
        super(CompteGestionDepenseFormSansArticle, self).__init__(*args, **kwargs)


class CompteAdmDepenseFormSansArticle(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtDepense
        #fields = '__all__'
        fields = ('ca_bud_primitif', 'ca_ae_speciale', 'ca_virement_credits', 'ca_droit_constate', 'ca_somme_payee', 'ca_rap', 'ca_denl', 'ca_cp_annule', 'ca_cp_invest_report')
        labels = {
            "ca_bud_primitif": "Budget Primitif",
            "ca_ae_speciale": "Autorisation spéciale",
            "ca_virement_credits": "Virements de crédits",
            "ca_droit_constate": "Droits constatés",
            "ca_somme_payee": "Sommes Payées",
            "ca_rap": "Restes à payer",
            "ca_denl": "Depenses engagées non liquidées",
            "ca_cp_annule": "Crédits annulés faute d'emploi",
            "ca_cp_invest_report": "Crédits d'investissement à reporter",
        }
    def __init__(self, *args, **kwargs):
        super(CompteAdmDepenseFormSansArticle, self).__init__(*args, **kwargs)
        

class CompteGestionDepenseForm(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtDepense
        #fields = '__all__'
        fields = ('budget_article', 'cg_bud_primitif', 'cg_ae_speciale', 'cg_virement_credits', 'cg_montant_pris_en_charge', 'cg_reglement')
        labels = {
            "budget_article": "Compte",
            "cg_bud_primitif": "Budget Primitif",
            "cg_ae_speciale": "Autorisation spéciale",
            "cg_virement_credits": "Virements de crédits",
            "cg_montant_pris_en_charge": "Montant pris en charge",
            "cg_reglement": "Règlement",
        }
    def __init__(self, *args, **kwargs):
        super(CompteGestionDepenseForm, self).__init__(*args, **kwargs)
        mouvements = BudgetArticleMvtDepense.objects.all()
        list_article_mv = []
        for m in mouvements:
            list_article_mv.append(m.budget_article.code)
        list_article_mv = []
        self.fields['budget_article'] = forms.ModelChoiceField(queryset=BudgetArticle.objects.filter(type_article='2').exclude(code__in=list_article_mv))

class CompteAdmDepenseForm(forms.ModelForm):
    
    class Meta:
        model = BudgetArticleMvtDepense
        #fields = '__all__'
        fields = ('budget_article', 'ca_bud_primitif', 'ca_ae_speciale', 'ca_virement_credits', 'ca_droit_constate', 'ca_somme_payee', 'ca_rap', 'ca_denl', 'ca_cp_annule', 'ca_cp_invest_report')
        labels = {
            "budget_article": "Compte",
            "ca_bud_primitif": "Budget Primitif",
            "ca_ae_speciale": "Autorisation spéciale",
            "ca_virement_credits": "Virements de crédits",
            "ca_droit_constate": "Droits constatés",
            "ca_somme_payee": "Sommes Payées",
            "ca_rap": "Restes à payer",
            "ca_denl": "Dépenses engagées non liquidées",
            "ca_cp_annule": "Crédits annulés faute d'emploi",
            "ca_cp_invest_report": "Crédits d'investissement à reporter",
        }
    def __init__(self, *args, **kwargs):
        super(CompteAdmDepenseForm, self).__init__(*args, **kwargs)
        mouvements = BudgetArticleMvtDepense.objects.all()
        list_article_mv = []
        for m in mouvements:
            list_article_mv.append(m.budget_article.code)
        list_article_mv = []
        self.fields['budget_article'] = forms.ModelChoiceField(queryset=BudgetArticle.objects.filter(type_article='2').exclude(code__in=list_article_mv))