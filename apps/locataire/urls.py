from django.urls import path
from .views import locataireView

urlpatterns = [
    path(
        "",
        locataireView.as_view(template_name="locataire.html"),
        name="locataire",
    ),
    path(
        "locataire/list/",
        locataireView.as_view(template_name="locataire_list.html"),
        name="locataire",
    )
]
