from django.urls import path
from . import views
from .views import HomeView,ConsultationView, LocataireView,StatsView, BailleurView, LocalisationView, ContratView, ImmeubleView, OccupantsView,Dossiers_ReglementsView,AvenantsView

app_name = 'baux'
urlpatterns = [
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    #path("bailleur/add/", views.bailleur, name='bailleur'),
    path("bailleur/add/", BailleurView.as_view(template_name="baux/bailleur.html"), name='bailleur'),
    path("bailleur/list/", BailleurView.as_view(template_name="baux/bailleur_list.html"), name='bailleur_list'),
    #path("immeuble/add/", views.immeuble, name='immeuble'),
    path("immeuble/add/", ImmeubleView.as_view(template_name="baux/immeuble.html"), name='immeuble'),
    path("immeuble/list/", ImmeubleView.as_view(template_name="baux/immeuble_list.html"), name='immeuble_list'),
    #path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    #path("contrat/add/", views.contrat, name='contrat'),
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    #path("contrat/<int:pk>/edit/", ContratUpdateView.as_view(), name='contrat_edit'),
    #path("contrat/<int:pk>/delete/", ContratDeleteView.as_view(), name='contrat_delete'),"""
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
    path("dossier_reglement/add/", Dossiers_ReglementsView.as_view(template_name="baux/dossier_reglement.html"), name='dossier_reglement'),
    path("dossier_reglement/list/", Dossiers_ReglementsView.as_view(template_name="baux/dossier_reglement_list.html"), name='dossier_reglement_list'),
    # avenants : 
    path("avenant/add/", AvenantsView.as_view(template_name="baux/avenant.html"), name='avenant'),
    path("avenant/list/", AvenantsView.as_view(template_name="baux/avenant_list.html"), name='avenant_list'),
    # consultation : 
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),
    # Statistiques : 
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),

]
