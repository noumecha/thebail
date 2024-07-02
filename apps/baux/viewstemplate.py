from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from crispy_bootstrap5.bootstrap5 import FloatingField
#from django.contrib.auth.mixins import LoginRequiredMixin

from .models import BudgetEntite, BudgetExecution, BudgetArticle, BudgetArticleMvtDepense, BudgetArticleMvtRecette
from .forms import (
    CompteAdmDepenseForm,
    CompteGestionDepenseForm, 
    CompteGestionRecetteForm, 
    CompteAdmRecetteForm, 
    CompteAdmRecetteFormSansArticle, 
    CompteGestionRecetteFormSansArticle,
    CompteGestionDepenseFormSansArticle,
    CompteAdmDepenseFormSansArticle,
    ControleCompteAdmForm,
    ControleCompteGestionForm,
)

# Create your views here.

#class EntiteList(LoginRequiredMixin, ListView):

class EntiteList(ListView):
    model = BudgetEntite
    context_object_name = 'budget_entites'
    
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entites'] = context['budget_entites'].all()
        return context

# Afficher la liste des executions d'une entite
@login_required(login_url="/login")
def budget_execution_list(request, budget_entite_id):
    budget_entite = BudgetEntite.objects.get(pk=budget_entite_id)
    
    return render(request, "infocentre/budget_execution_list.html", {
        "budget_entite": BudgetEntite.objects.get(pk=budget_entite.id),
        "budget_executions": BudgetExecution.objects.filter(budget_entite=budget_entite)
    })
# Afficher dashboard infocentre
@login_required(login_url="/login")
def dashboard(request):
    return render(request, "infocentre/dashboard.html", {
    })
# Afficher les saisies effectuees sur le compte administratif
@login_required(login_url="/login")
def display_compte_depense(request, type_compte, execution_id):
    budget_execution = BudgetExecution.objects.get(pk=execution_id)
    if type_compte == 1:
        url_compte = "infocentre-saisie-compte-adm-depense"
    else:
        url_compte = "infocentre-saisie-compte-adm-depense"

    return render(request, "infocentre/display_compte_depense.html", {
        "budget_execution": BudgetExecution.objects.get(pk=budget_execution.id),
        "type_compte": type_compte,
        "url_compte": url_compte,
        "mvt_compte_depense_list": BudgetArticleMvtDepense.objects.filter(budget_execution=budget_execution)
    })

# Afficher les saisies effectuees sur le compte administratif
@login_required(login_url="/login")
def display_compte_recette(request, type_compte, execution_id):
    budget_execution = BudgetExecution.objects.get(pk=execution_id)
    if type_compte == 1:
        url_compte = "infocentre-saisie-compte-adm-recette"
    else:
        url_compte = "infocentre-saisie-compte-adm-recette"

    return render(request, "infocentre/display_compte_recette.html", {
        "budget_execution": BudgetExecution.objects.get(pk=budget_execution.id),
        "type_compte": type_compte,
        "url_compte": url_compte,
        "mvt_compte_recette_list": BudgetArticleMvtRecette.objects.filter(budget_execution=budget_execution)
    })

# la vue de la saisie doit contenir l'exercice et AP dont on est en train de saisir le CG ou CG
@login_required(login_url="/login")
def compte_adm_depense(request, execution_id):
    #execution_instance = get_object_or_404(BudgetExecution, execution_id)
    execution_instance = BudgetExecution.objects.get(pk=execution_id)

    if request.method == 'GET':
        form = CompteAdmDepenseForm()

        context = {
            'form': form,
            'execution_instance': execution_instance
        }

        return render(request, 'infocentre/compte_adm_depense.html', context)
    # If this a POST request then process the form data
    elif request.method == 'POST':

        budget_article_id = request.POST['budget_article']
        budget_article = BudgetArticle.objects.get(pk=budget_article_id)

        budget_execution_id = request.POST['budget_execution']
        budget_execution = BudgetExecution.objects.get(pk=budget_execution_id)
        # Check if the line already exists, then update
        mouvements = BudgetArticleMvtDepense.objects.filter(budget_article=budget_article).filter(budget_execution=budget_execution)
        if mouvements:
            # create the form instance and populate it with data from the request(binding)
            form = CompteAdmDepenseForm(request.POST, instance=mouvements[0])
        else:
            # create the form instance and populate it with data from the request(binding)
            form = CompteAdmDepenseForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            
            if mouvements:
                compte_adm_depense = form.save()
            else:
                compte_adm_depense = form.save(commit=False)
                compte_adm_depense.budget_execution = budget_execution
                compte_adm_depense.save()
            messages.success(request, f'Enregistrement effectue avec succes.')

            # Reload the registration form
            form = CompteAdmDepenseForm()

            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            return render(request, 'infocentre/compte_adm_depense.html', context)
        else:
            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            messages.error(request, f'Echec d''enregistrement')
            return render(request, 'infocentre/compte_adm_depense.html', context)

# la vue de la saisie doit contenir l'exercice et AP dont on est en train de saisir le CG ou CG
@login_required(login_url="/login")
def saisie_compte_depense(request, type_compte, execution_id):
    #execution_instance = get_object_or_404(BudgetExecution, execution_id)
    execution_instance = BudgetExecution.objects.get(pk=execution_id)

    if type_compte == 1:
        link = 'infocentre/compte_gestion_depense.html'
    else:
        link = 'infocentre/compte_adm_depense.html'

    if request.method == 'GET':
        if type_compte == 1:
            form = CompteGestionDepenseFormSansArticle()
        else:
            form = CompteAdmDepenseFormSansArticle()

        context = {
            'form': form,
            'execution_instance': execution_instance
        }

        return render(request, link, context)
    # If this a POST request then process the form data
    elif request.method == 'POST':

        budget_article_id = request.POST['budget_article']
        budget_article = BudgetArticle.objects.get(pk=budget_article_id)

        budget_execution_id = request.POST['budget_execution']
        budget_execution = BudgetExecution.objects.get(pk=budget_execution_id)
        # Check if the line already exists, then update
        mouvements = BudgetArticleMvtDepense.objects.filter(budget_article=budget_article).filter(budget_execution=budget_execution)
        if mouvements:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionDepenseFormSansArticle(request.POST, instance=mouvements[0])
            else:
                form = CompteAdmDepenseFormSansArticle(request.POST, instance=mouvements[0])
        else:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionDepenseFormSansArticle(request.POST)
            else:
                form = CompteAdmDepenseFormSansArticle(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            
            if mouvements:
                compte_depense = form.save()
            else:
                compte_depense = form.save(commit=False)
                compte_depense.budget_execution = budget_execution
                compte_depense.budget_article = budget_article
                compte_depense.save()
            messages.success(request, f'Enregistrement effectue avec succes.')

            # Reload the registration form
            if type_compte == 1:
                form = CompteGestionDepenseFormSansArticle()
            else:
                form = CompteAdmDepenseFormSansArticle()

            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            return render(request, link, context)
        else:
            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            messages.error(request, f'Echec d''enregistrement')
            return render(request, link, context)



# la vue de la saisie doit contenir l'exercice et AP dont on est en train de saisir le CG ou CG
@login_required(login_url="/login")
def saisie_compte_recette(request, type_compte, execution_id):
    #execution_instance = get_object_or_404(BudgetExecution, execution_id)
    execution_instance = BudgetExecution.objects.get(pk=execution_id)

    if type_compte == 1:
        link = 'infocentre/compte_gestion_recette.html'
    else:
        link = 'infocentre/compte_adm_recette.html'

    if request.method == 'GET':
        if type_compte == 1:
            form = CompteGestionRecetteFormSansArticle()
        else:
            form = CompteAdmRecetteFormSansArticle()

        context = {
            'form': form,
            'execution_instance': execution_instance
        }

        return render(request, link, context)
    # If this a POST request then process the form data
    elif request.method == 'POST':

        budget_article_id = request.POST['budget_article']
        budget_article = BudgetArticle.objects.get(pk=budget_article_id)

        budget_execution_id = request.POST['budget_execution']
        budget_execution = BudgetExecution.objects.get(pk=budget_execution_id)
        # Check if the line already exists, then update
        mouvements = BudgetArticleMvtRecette.objects.filter(budget_article=budget_article).filter(budget_execution=budget_execution)
        if mouvements:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionRecetteFormSansArticle(request.POST, instance=mouvements[0])
            else:
                form = CompteAdmRecetteFormSansArticle(request.POST, instance=mouvements[0])
        else:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionRecetteFormSansArticle(request.POST)
            else:
                form = CompteAdmRecetteFormSansArticle(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            
            if mouvements:
                compte_recette = form.save()
            else:
                compte_recette = form.save(commit=False)
                compte_recette.budget_execution = budget_execution
                compte_recette.budget_article = budget_article
                compte_recette.save()
            messages.success(request, f'Enregistrement effectue avec succes.')

            # Reload the registration form
            if type_compte == 1:
                form = CompteGestionRecetteFormSansArticle()
            else:
                form = CompteAdmRecetteFormSansArticle()

            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            return render(request, link, context)
        else:
            context = {
                'form': form,
                'execution_instance': execution_instance
            }

            messages.error(request, f'Echec d''enregistrement')
            return render(request, link, context)

# Afficher les saisies effectuees sur le compte administratif
@login_required(login_url="/login")
def upd_compte_recette(request, type_compte, execution_mvt_id):
    #execution_instance = get_object_or_404(BudgetExecution, execution_id)
    execution_mvt_instance = BudgetArticleMvtRecette.objects.get(pk=execution_mvt_id)

    if type_compte == 1:
        link = 'infocentre/upd_compte_recette.html'
    else:
        link = 'infocentre/upd_compte_recette.html'

    if request.method == 'GET':

        if type_compte == 1:
            form = CompteGestionRecetteForm(instance=execution_mvt_instance)
        else:
            form = CompteAdmRecetteForm(instance=execution_mvt_instance)

        context = {
            'form': form,
            'execution_mvt_instance': execution_mvt_instance
        }

        return render(request, link, context)
    # If this a POST request then process the form data
    elif request.method == 'POST':
        # Check if the line already exists, then update
        if execution_mvt_instance:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionRecetteForm(request.POST, instance=execution_mvt_instance)
            else:
                form = CompteAdmRecetteForm(request.POST, instance=execution_mvt_instance)
        else:
            messages.error(request, f'Enregistrement inexistant.')

            # Reload the registration form
            if type_compte == 1:
                form = CompteGestionRecetteForm()
            else:
                form = CompteAdmRecetteForm()

            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            return render(request, link, context)

        # Check if the form is valid:
        if form.is_valid():
            compte_adm_depense = form.save()
            messages.success(request, f'Mise a jour effectuee avec succes.')

            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            return render(request, link, context)
        else:
            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            messages.error(request, f'Echec de la mise a jour')
            return render(request, link, context)

# Afficher les saisies effectuees sur le compte administratif
@login_required(login_url="/login")
def upd_compte_depense(request, type_compte, execution_mvt_id):
    #execution_instance = get_object_or_404(BudgetExecution, execution_id)
    execution_mvt_instance = BudgetArticleMvtDepense.objects.get(pk=execution_mvt_id)

    if type_compte == 1:
        link = 'infocentre/upd_compte_depense.html'
    else:
        link = 'infocentre/upd_compte_depense.html'

    if request.method == 'GET':

        if type_compte == 1:
            form = CompteGestionDepenseForm(instance=execution_mvt_instance)
        else:
            form = CompteAdmDepenseForm(instance=execution_mvt_instance)

        context = {
            'form': form,
            'execution_mvt_instance': execution_mvt_instance
        }

        return render(request, link, context)
    # If this a POST request then process the form data
    elif request.method == 'POST':
        # Check if the line already exists, then update
        if execution_mvt_instance:
            # create the form instance and populate it with data from the request(binding)
            if type_compte == 1:
                form = CompteGestionDepenseForm(request.POST, instance=execution_mvt_instance)
            else:
                form = CompteAdmDepenseForm(request.POST, instance=execution_mvt_instance)
        else:
            messages.error(request, f'Enregistrement inexistant.')

            # Reload the registration form
            if type_compte == 1:
                form = CompteGestionDepenseForm()
            else:
                form = CompteAdmDepenseForm()

            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            return render(request, link, context)

        # Check if the form is valid:
        if form.is_valid():
            compte_adm_depense = form.save()
            messages.success(request, f'Mise a jour effectuee avec succes.')

            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            return render(request, link, context)
        else:
            context = {
                'form': form,
                'execution_mvt_instance': execution_mvt_instance
            }

            messages.error(request, f'Echec de la mise a jour')
            return render(request, link, context)
# Le contrôle consiste a saisir les montants correspondants aux sommes sur chaque colonne 
# et ensuite, verifier que les montants saisis sont correspondent aux sommes saisies
def controle_compte_adm(request, execution_id):
    execution_instance = BudgetExecution.objects.get(pk=execution_id)

    if request.method == 'GET':
        return render(request, 'infocentre/controle_compte_adm.html', 
        {
            'execution_instance': execution_instance,
            'form': ControleCompteAdmForm(instance=execution_instance)
        })
    elif request.method == 'POST':
        form = ControleCompteAdmForm(request.POST, instance=execution_instance)
        if form.is_valid():
            # ici on va calculer les sommes des saisies par colonne
            # avec une requete SELECT sum(*)
            sum_mvt_depense = BudgetArticleMvtDepense.objects.filter(budget_execution=execution_instance).aggregate(
                Sum("ca_bud_primitif"),
                Sum("ca_ae_speciale"), 
                Sum("ca_droit_constate"), 
                Sum("ca_somme_payee"), 
                Sum("ca_rap"), 
                Sum("ca_denl"), 
                Sum("ca_cp_annule"), 
                Sum("ca_cp_invest_report")
            )
            sum_mvt_recette = BudgetArticleMvtRecette.objects.filter(budget_execution=execution_instance).aggregate(
                Sum("ca_bud_primitif"),
                Sum("ca_virement"), 
                Sum("ca_emission"), 
                Sum("ca_recouvrement"), 
                Sum("ca_anv"), 
                Sum("ca_rr_r"), 
                Sum("ca_rr_d"), 
                Sum("ca_rr_ir")
            )

            return render(request, 'infocentre/validate_compte_adm.html', 
                {
                    'execution_instance': execution_instance,
                    'form': form,
                    'sum_mvt_recette': sum_mvt_recette,
                    'sum_mvt_depense': sum_mvt_depense
                })
        else:
            return render(request, 'infocentre/controle_compte_adm.html', 
                {
                    'execution_instance': execution_instance,
                    'form': form
                })

# Le contrôle consiste a saisir les montants correspondants aux sommes sur chaque colonne 
# et ensuite, verifier que les montants saisis sont correspondent aux sommes saisies
@login_required(login_url="/login")
def controle_compte_gestion(request, execution_id):
    execution_instance = BudgetExecution.objects.get(pk=execution_id)

    if request.method == 'GET':
        return render(request, 'infocentre/controle_compte_gestion.html', 
            {
                'execution_instance': execution_instance,
                'form': ControleCompteGestionForm(instance=execution_instance)
            })
    elif request.method == 'POST':
        form = ControleCompteGestionForm(request.POST, instance=execution_instance)
        if form.is_valid():
            # ici on va calculer les sommes des saisies par colonne
            # avec une requete SELECT sum(*)
            sum_mvt_depense = BudgetArticleMvtDepense.objects.filter(budget_execution=execution_instance).aggregate(
                Sum("ca_bud_primitif"),
                Sum("ca_ae_speciale"), 
                Sum("cg_virement_credits"), 
                Sum("cg_montant_pris_en_charge"), 
                Sum("cg_reglement")
            )
            sum_mvt_recette = BudgetArticleMvtRecette.objects.filter(budget_execution=execution_instance).aggregate(
                Sum("cg_bud_primitif"),
                Sum("cg_virement"), 
                Sum("cg_emission"), 
                Sum("cg_recouvrement"), 
                Sum("cg_anv"), 
                Sum("cg_rr_r"), 
                Sum("cg_rr_d"), 
                Sum("cg_rr_ir")
            )
            
            return render(request, 'infocentre/validate_compte_gestion.html',
            {
                'execution_instance': execution_instance,
                'form': form,
                'sum_mvt_recette': sum_mvt_recette,
                'sum_mvt_depense': sum_mvt_depense
            })
        else:
            return render(request, 'infocentre/controle_compte_gestion.html', 
                {
                    'execution_instance': execution_instance,
                    'form': form
                })

# fonction de validation du compte administratif
@login_required(login_url="/login")
def validate_compte_adm(request, execution_id):

    if request.method == "POST":
        execution_instance = BudgetExecution.objects.get(pk=execution_id)
        form = ControleCompteAdmForm(request.POST, instance=execution_instance)
        # ici on va calculer les sommes des saisies par colonne
        # avec une requete SELECT sum(*)
        sum_mvt_recette = BudgetArticleMvtRecette.objects.filter(budget_execution=execution_instance).aggregate(
            Sum("ca_bud_primitif"),
            Sum("ca_virement"), 
            Sum("ca_emission"), 
            Sum("ca_recouvrement"), 
            Sum("ca_anv"), 
            Sum("ca_rr_r"), 
            Sum("ca_rr_d"), 
            Sum("ca_rr_ir")
        )
        sum_mvt_depense = BudgetArticleMvtDepense.objects.filter(budget_execution=execution_instance).aggregate(
            Sum("ca_bud_primitif"),
            Sum("ca_ae_speciale"), 
            Sum("ca_droit_constate"), 
            Sum("ca_somme_payee"), 
            Sum("ca_rap"), 
            Sum("ca_denl"), 
            Sum("ca_cp_annule"), 
            Sum("ca_cp_invest_report")
        )
        context = {
                'execution_instance': execution_instance,
                'form': form,
                'sum_mvt_recette': sum_mvt_recette,
                'sum_mvt_depense': sum_mvt_depense
            }
        if form.is_valid():
            # calculate the hash
            hash = 0
            hash += form.instance.ca_rr_bud_primitif - sum_mvt_recette.ca_bud_primitif
            hash += form.instance.ca_rr_virement - sum_mvt_recette.ca_virement
            hash += form.instance.ca_rr_emission - sum_mvt_recette.ca_emission
            hash += form.instance.ca_rr_recouvrement - sum_mvt_recette.ca_recouvrement
            hash += form.instance.ca_rr_anv - sum_mvt_recette.ca_anv
            hash += form.instance.ca_rr_r - sum_mvt_recette.ca_rr_r
            hash += form.instance.ca_rr_d - sum_mvt_recette.ca_rr_d
            hash += form.instance.ca_rr_ir - sum_mvt_recette.ca_rr_ir
            hash += form.instance.ca_dd_bud_primitif - sum_mvt_depense.ca_bud_primitif
            hash += form.instance.ca_dd_ae_speciale - sum_mvt_depense.ca_ae_speciale
            hash += form.instance.ca_dd_droit_constate - sum_mvt_depense.ca_droit_constate
            hash += form.instance.ca_dd_somme_payee - sum_mvt_depense.ca_somme_payee
            hash += form.instance.ca_dd_rap - sum_mvt_depense.ca_rap
            hash += form.instance.ca_dd_denl - sum_mvt_depense.ca_denl
            hash += form.instance.ca_dd_cp_annule - sum_mvt_depense.ca_cp_annule
            hash += form.instance.ca_dd_cp_invest_report - sum_mvt_depense.ca_cp_invest_report
            if hash == 0:
                form.save()
                messages.succes(request, f'Validation du compte administratif effectue avec succes')
                return render(request, 'infocentre/validate_compte_adm.html', context)
            else:
                messages.error(request, f'Echec de validation: les montants ne correspondent pas')
                return render(request, 'infocentre/validate_compte_adm.html', context)
        else:
            messages.error(request, f'Echec de validation: formulaire invalide')
            return render(request, 'infocentre/validate_compte_adm.html', context)
        
@login_required(login_url="/login")
def validate_compte_gestion(request, execution_id):
    pass

