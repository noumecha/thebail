from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import AccessoireView,AccessoireDeleteView,HomeView,AvenantsDeleteView,LocataireDeleteView, ConsultationView,LocalisationDeleteView, BailleurDeleteView, OccupantsDeleteView, LocataireView,StatsView,Non_MandatementDeleteView,  BailleurView, AvenantsDeleteView, LocalisationView, ContratView, ImmeubleView, ImmeubleDeleteView,OccupantsView,Non_MandatementView,AvenantsView,ContratDeleteView,ContratUpdateView

app_name = 'baux'
urlpatterns = [
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    #path("bailleur/add/", views.bailleur, name='bailleur'),
    path("bailleur/add/", BailleurView.as_view(template_name="baux/bailleur.html"), name='bailleur'),
    path("bailleur/list/", BailleurView.as_view(template_name="baux/bailleur_list.html"), name='bailleur_list'),
    path("bailleur/delete/<int:pk>/", BailleurDeleteView.as_view(), name='bailleur_delete'),
    path("bailleur/update/<int:pk>/", BailleurView.as_view(template_name="baux/bailleur.html"), name='bailleur_update'),
    #path("immeuble/add/", views.immeuble, name='immeuble'),
    path("immeuble/add/", ImmeubleView.as_view(template_name="baux/immeuble.html"), name='immeuble'),
    path("immeuble/list/", ImmeubleView.as_view(template_name="baux/immeuble_list.html"), name='immeuble_list'),
    path("immeuble/accessoire/", AccessoireView.as_view(template_name="baux/immeuble_accessoire.html"), name='immeuble_accessoire'),
    path("accessoire/update/<int:pk>", AccessoireView.as_view(template_name="baux/immeuble_accessoire.html"), name='accessoire_update'),
    path("accessoire/delete/<int:pk>", AccessoireDeleteView.as_view(), name='accessoire_delete'),
    path("immeuble/delete/<int:pk>/", ImmeubleDeleteView.as_view(), name='immeuble_delete'),
    path("immeuble/update/<int:pk>/", ImmeubleView.as_view(template_name="baux/immeuble.html"), name='immeuble_update'),
    #path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    #path("contrat/add/", views.contrat, name='contrat'),
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    path("contrat/delete/<int:pk>/", ContratDeleteView.as_view(), name='contrat_delete'),
    path("contrat/update/<int:pk>/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat_update'),
    #path("locataire/add/", views.locataire, name='locataire'),
    path("locataire/add/", LocataireView.as_view(template_name="baux/locataire.html"), name='locataire'),
    path("locataire/list/", LocataireView.as_view(template_name="baux/locataire_list.html"), name='locataire_list'),
    path("locataire/delete/<int:pk>/", LocataireDeleteView.as_view(), name='locataire_delete'),
    path("locataire/update/<int:pk>/", LocataireView.as_view(template_name="baux/locataire.html"), name='locataire_update'),
    #path("localisation/add/", views.localisation, name='localisation'),
    path("localisation/add/", LocalisationView.as_view(template_name="baux/localisation.html"), name='localisation'),
    path("localisation/list/", LocalisationView.as_view(template_name="baux/localisation_list.html"), name='localisation_list'),
    path("localisation/delete/<int:pk>/", LocalisationDeleteView.as_view(), name='localisation_delete'),
    path("localisation/update/<int:pk>/", LocalisationView.as_view(template_name="baux/localisation.html"), name='localisation_update'),
    #routes for occupants
    path("occupants/add/", OccupantsView.as_view(template_name="baux/occupants.html"), name='occupants'),
    path("occupants/list/", OccupantsView.as_view(template_name="baux/occupants_list.html"), name='occupants_list'),
    path("occupants/delete/<int:pk>/", OccupantsDeleteView.as_view(), name='occupants_delete'),
    path("occupants/update/<int:pk>/", OccupantsView.as_view(template_name="baux/occupants.html"), name='occupants_update'),
    # dossier reglements : 
    path("non_mandatement/add/", Non_MandatementView.as_view(template_name="baux/non_mandatement.html"), name='non_mandatement'),
    path("non_mandatement/list/", Non_MandatementView.as_view(template_name="baux/non_mandatement_list.html"), name='non_mandatement_list'),
    path("non_mandatement/delete/<int:pk>/", Non_MandatementDeleteView.as_view(), name='non_mandatement_delete'),
    path("non_mandatement/update/<int:pk>/", Non_MandatementView.as_view(template_name="baux/non_mandatement.html"), name='non_mandatement_update'),
    # avenants : 
    path("avenant/add/", AvenantsView.as_view(template_name="baux/avenant.html"), name='avenant'),
    path("avenant/list/", AvenantsView.as_view(template_name="baux/avenant_list.html"), name='avenant_list'),
    path("avenant/delete/<int:pk>/", AvenantsDeleteView.as_view(), name='avenant_delete'),
    path("avenant/update/<int:pk>/", AvenantsView.as_view(template_name="baux/avenant.html"), name='avenant_update'),
    # consultation : 
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),
    # Statistiques : 
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),

]

#debuging images : 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)