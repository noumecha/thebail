from django.urls import path
from .views import bailleurView
from . import views

urlpatterns = [
    path(
        "bailleur/add/",
        bailleurView.as_view(template_name="bailleur.html"),
        name="bailleur-add",
    ),
    path(
        "bailleur/list/",
        bailleurView.as_view(template_name="bailleur_list.html"),
        name="bailleur-list",
    )
]