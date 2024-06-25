from django.urls import path
from .views import locataireView
from . import views

urlpatterns = [
    path(
        "locataire/add/",
        locataireView.as_view(template_name="locataire.html"),
        name="locataire-add",
    ),
    path(
        "locataire/list/",
        locataireView.as_view(template_name="locataire_list.html"),
        name="locataire-list",
    )
]
