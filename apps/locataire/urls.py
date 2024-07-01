from django.urls import path
from .views import LocataireView
from . import views

urlpatterns = [
    path(
        "locataire/add/",
        LocataireView.as_view(template_name="locataire.html"),
        name="locataire-add",
    ),
    path(
        "locataire/list/",
        LocataireView.as_view(template_name="locataire_list.html"),
        name="locataire-list",
    ),
    #path(
    #    "locataire/new/",
    #    LocataireCreateView.as_view(template_name="locataire_new.html"),
    #    name="locataire-new",
    #)
]
