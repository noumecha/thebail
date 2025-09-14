from django.urls import path
from . import views
from django.contrib import admin
from .views import *
from django.urls import re_path as url

app_name = 'baux'

# crud urls helper 
def get_crud_urls(view_class, prefix, name):
    """ Helper function to generate CRUD URLs for a view class """
    #name = view_class.model._meta.model_name
    return [
        path(f"{prefix}/", view_class.as_view(template_name=view_class.list_template), name=f'{name}_list'),
        path(f"{prefix}/all/", view_class.as_view(), {'action': 'list'}, name=f'get_{name}s'),
        path(f"{prefix}/form/", view_class.as_view(), {'action': 'form'}, name=f'{name}_form'),
        path(f"{prefix}/edit/<int:pk>", view_class.as_view(), {'action': 'form'}, name=f'{name}_update'),
        path(f"{prefix}/update/<int:pk>", view_class.as_view(), {'action': 'update'}, name=f'{name}_update'),
        path(f"{prefix}/delete/<int:pk>", view_class.as_view(), {'action': 'delete'}, name=f'{name}_delete'),
    ]

# urls
urlpatterns = [
    *get_crud_urls(LocataireView, "locataire/locataires", "locataire"),
    *get_crud_urls(BailleurView, "bailleur/bailleurs", "bailleur"),
    *get_crud_urls(ImmeubleView, "immeuble/immeubles", "immeuble"),
    *get_crud_urls(views.RecensementView, "immeuble/recensements", "recensement"),
    *get_crud_urls(TypeConstructionsView, "typeconstruction/typeconstructions", "typeconstruction"),
    *get_crud_urls(Non_MandatementView, "non_mandatement/non_mandatements", "non_mandatement"),
    *get_crud_urls(LocalisationView, "localisation/localisations", "localisation"),
    *get_crud_urls(OccupantsView, "occupant/occupants", "occupant"),
    *get_crud_urls(AvenantsView, "avenant/avenants", "avenant"),
    *get_crud_urls(views.TypeContratView, "typecontrat/typecontrats", "typecontrat"),
    # revetements urls
    *get_crud_urls(RevetementIntsView, "revetementint/revetementints", "revetementint"),
    *get_crud_urls(RevetementExtsView, "revetementext/revetementexts", "revetementext"),
    # 
    *get_crud_urls(ElementDeDescriptionView, "elementdescription/elementdescriptions", "elementdescription"),
    *get_crud_urls(PieceView, "piece/pieces", "piece"),
    # 
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    # type contrant partial 
    path('type-contrat-partial-form/', views.typecontrat_partial_form_view, name='type_contrat_partial_form'),
    # bailleur routes 
    path('bailleur-partial-form/', views.bailleur_partial_form_view, name='bailleur_partial_form'),
    # locataire routes
    #path('locataire-partial-form/', views._partial_form_view, name='locataire_partial_form'),
    path('immeuble-partial-form/', views.immeuble_partial_form_view, name='immeuble_partial_form'), # for modal purpose
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    # autocomplete on contrat form
    path( "service/autocomplete/", ServiceAutocomplete.as_view(), name="service_autocomplete",),
    path('structure/autocomplete/', StructureAutocomplete.as_view(), name='structure_autocomplete'),
    path('admins-beneficiaire/autocomplete/', AdminAutocomplete.as_view(), name='administration_beneficiaire_autocomplete'),
    path('bailleur/autocomplete/', BailleurAutocomplete.as_view(), name='bailleur_autocomplete'),
    # contrat urls
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    path("contrat/print/<int:pk>/", ContratView.print_contrat, name='contrat_print'),
    path("contrat/delete/<int:pk>/", ContratDeleteView.as_view(), name='contrat_delete'),
    path("contrat/update/<int:pk>/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat_update'),
    path("structures/", views.get_structures, name='get_structures'),  # for filtering structures based on administration <int:administration_id>
    # consultation : 
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),
    # Statistiques : 
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),
    # collecte : 
    path('collecte/add/', CollecteView.as_view(template_name="baux/collecte.html"), name='collecte'),
    path("collecte/list/", CollecteView.as_view(template_name="baux/collecte_list.html"), name='collecte_list'),
    #path("collecte/print/<int:pk>/", ContratView.print_contrat, name='collecte_print'),
    #path("collecte/delete/<int:pk>/", ContratDeleteView.as_view(), name='collecte_delete'),
    #path("collecte/update/<int:pk>/", ContratView.as_view(template_name="baux/collecte.html"), name='collecte_update'),
]
