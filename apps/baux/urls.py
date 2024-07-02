from django.urls import path

from .import views 

# from .api_views import BudgetArticleApiView, BudgetArticleMvtDepenseApiView

app_name = 'baux'
urlpatterns = [
    #path('infocentre/', EntiteList.as_view(), name='infocentre-entites'),

    path("baux", views.index, name='Home'),
    path("bailleur", views.bailleur, name='bailleur'),
    path("immeuble", views.immeuble, name='immeuble'),
    path("Menuimmeuble", views.Menuimmeuble, name='Menuimmeuble'),
    path("contrat", views.contrat, name='contrat'),
    path("locataire", views.locataire, name='locataire'),
    path("localisation", views.localisation, name='localisation'),


]
