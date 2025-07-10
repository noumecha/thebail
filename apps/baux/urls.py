from django.urls import path
from . import views
from .views import TypeContratView,CollecteView,HomeView,ConsultationView, LocataireView,StatsView, BailleurView, LocalisationView, ContratView, ImmeubleView, OccupantsView,Non_MandatementView,AvenantsView,ContratDeleteView,ContratUpdateView
from .forms import LocatairesForm,AccessoiresForm, BailleursForm

app_name = 'baux'
urlpatterns = [
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    #path("bailleur/add/", views.bailleur, name='bailleur'),
    path("bailleur/add/", BailleurView.as_view(template_name="baux/bailleur.html"), name='bailleur'),
    path("bailleur/list/", BailleurView.as_view(template_name="baux/bailleur_list.html"), name='bailleur_list'),
    path('bailleur-partial-form/', views.bailleur_partial_form_view, name='bailleur_partial_form'), # for modal purpose
    #path("immeuble/add/", views.immeuble, name='immeuble'),
    path("immeuble/add/", ImmeubleView.as_view(template_name="baux/immeuble.html"), name='immeuble'),
    path("immeuble/list/", ImmeubleView.as_view(template_name="baux/immeuble_list.html"), name='immeuble_list'),
    path('immeuble-partial-form/', views.immeuble_partial_form_view, name='immeuble_partial_form'), # for modal purpose
    #path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    #path("contrat/add/", views.contrat, name='contrat'),
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    path("contrat/types/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_list'),
    path("contrat/update/<int:pk>/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_update'),
    path("contrat/delete/<int:pk>/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_delete'),
    path("contrat/types/form/", views.typecontrat_form_view, name='type_contrat_form'),  # for modal purpose
    path("structures/", views.get_structures, name='get_structures'),  # for filtering structures based on administration <int:administration_id>
    #path("contrat/print/<int:pk>/", ContratView.as_view(template_name="baux/docs/contrat_doc.html"), name='contrat_print'),
    path("contrat/print/<int:pk>/", ContratView.print_contrat, name='contrat_print'),
    path("contrat/delete/<int:pk>/", ContratDeleteView.as_view(), name='contrat_delete'),
    path("contrat/update/<int:pk>/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat_update'),
    #path("locataire/add/", views.locataire, name='locataire'),
    path("locataire/add/", LocataireView.as_view(template_name="baux/locataire.html"), name='locataire'),
    path("locataire/list/", LocataireView.as_view(template_name="baux/locataire_list.html"), name='locataire_list'),
    #path("localisation/add/", views.localisation, name='localisation'),
    path("localisation/add/", LocalisationView.as_view(template_name="baux/localisation.html"), name='localisation'),
    path("localisation/list/", LocalisationView.as_view(template_name="baux/localisation_list.html"), name='localisation_list'),
    #routes for occupants
    path("occupants/add/", OccupantsView.as_view(template_name="baux/occupants.html"), name='occupants'),
    path("occupants/list/", OccupantsView.as_view(template_name="baux/occupants_list.html"), name='occupants_list'),
    # dossier reglements : 
    path("non_mandatement/add/", Non_MandatementView.as_view(template_name="baux/non_mandatement.html"), name='non_mandatement'),
    path("non_mandatement/list/", Non_MandatementView.as_view(template_name="baux/non_mandatement_list.html"), name='non_mandatement_list'),
    # avenants : 
    path("avenant/add/", AvenantsView.as_view(template_name="baux/avenant.html"), name='avenant'),
    path("avenant/list/", AvenantsView.as_view(template_name="baux/avenant_list.html"), name='avenant_list'),
    # consultation : 
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),
    # Statistiques : 
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),
    # collecte : 
    path('collecte/add/', CollecteView.as_view([LocatairesForm,AccessoiresForm, BailleursForm]), name='collecte'),

]
