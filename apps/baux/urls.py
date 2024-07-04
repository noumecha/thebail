from django.urls import path
from . import views
from .views import LocataireView, BailleurView, LocalisationView, ContratView, ImmeubleView

# from .api_views import BudgetArticleApiView, BudgetArticleMvtDepenseApiView

app_name = 'baux'
urlpatterns = [
    #path('infocentre/', EntiteList.as_view(), name='infocentre-entites'),

    path("baux", views.index, name='Home'),
    #path("bailleur/add/", views.bailleur, name='bailleur'),
    path("bailleur/add/", BailleurView.as_view(template_name="baux/bailleur.html"), name='bailleur'),
    #path("immeuble/add/", views.immeuble, name='immeuble'),
    path("immeuble/add/", ImmeubleView.as_view(template_name="baux/immeuble.html"), name='immeuble'),
    #path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    #path("contrat/add/", views.contrat, name='contrat'),
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    #path("locataire/add/", views.locataire, name='locataire'),
    path("locataire/add/", LocataireView.as_view(template_name="baux/locataire.html"), name='locataire'),
    #path("localisation/add/", views.localisation, name='localisation'),
    path("localisation/add/", LocalisationView.as_view(template_name="baux/localisation.html"), name='localisation'),


]
