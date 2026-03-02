from django.urls import path
from django.contrib import admin

from apps.baux.views import api_bailleur_views, api_fiche_views, api_immeuble_views
from .views import *
from django.urls import re_path as url
from rest_framework.routers import DefaultRouter
from .views.fichecollecteviews import FicheCollecteViewSet, FicheCollecteFormView, FicheEditView
from django.conf.urls.static import static

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

# api routes
router = DefaultRouter()
router.register("fiches", FicheCollecteViewSet)

# partial form helper urls
def partial_form_urls(view_func, prefix, name):
    """ Helper function to generate partial form URL """
    return [
        path(f"{prefix}-partial-form/", view_func, name=f'{name}_partial_form'),
    ]
# urls
urlpatterns = [
    # cruds urls
    *get_crud_urls(LocataireView, "locataire/locataires", "locataire"),
    *get_crud_urls(BailleurView, "bailleur/bailleurs", "bailleur"),
    *get_crud_urls(ImmeubleView, "immeuble/immeubles", "immeuble"),
    *get_crud_urls(views.RecensementView, "immeuble/recensements", "recensement"),
    *get_crud_urls(TypeConstructionsView, "typeconstruction/typeconstructions", "typeconstruction"),
    *get_crud_urls(Non_MandatementView, "non_mandatement/non_mandatements", "non_mandatement"),
    *get_crud_urls(LocalisationView, "localisation/localisations", "localisation"),
    *get_crud_urls(OccupantsView, "occupant/occupants", "occupant"),
    *get_crud_urls(AvenantsView, "avenant/avenants", "avenant"),
    *get_crud_urls(TypeContratView, "typecontrat/typecontrats", "typecontrat"),
    *get_crud_urls(PeriodiciteReglementView, "periodiciterel/periodiciterels", "periodiciterel"),
    *get_crud_urls(views.ExercicesView, "exercice/exercices", "exercice"),
    *get_crud_urls(RevetementIntsView, "revetementint/revetementints", "revetementint"),
    *get_crud_urls(RevetementExtsView, "revetementext/revetementexts", "revetementext"),
    *get_crud_urls(ElementDeDescriptionView, "elementdescription/elementdescriptions", "elementdescription"),
    *get_crud_urls(PieceView, "piece/pieces", "piece"),

    # partial forms urls
    *partial_form_urls(TypeContratPartialFormView.as_view(), "type-contrat", "type_contrat"),
    *partial_form_urls(BailleursPartialFormView.as_view(), "bailleur", "bailleur"),
    *partial_form_urls(ExercicePartialFormView.as_view(), "exercice", "exercice"),
    *partial_form_urls(RevetementIntPartialFormView.as_view(), "revetement-ext", "revetementext"),
    *partial_form_urls(RevetementExtPartialFormView.as_view(), "revetement-int", "revetementint"),
    *partial_form_urls(ImmeublePartialFormView.as_view(), "immeuble", "immeuble"),
    *partial_form_urls(ElementPartialFormView.as_view(), "element-description", "elementdescription"),
    *partial_form_urls(PiecePartialFormView.as_view(), "piece-collecte", "piececollecte"),

    # specific partial form urls
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),

    # autocomplete on contrat form
    path("service/autocomplete/", ServiceAutocomplete.as_view(), name="service_autocomplete"),
    path('structure/autocomplete/', StructureAutocomplete.as_view(), name='structure_autocomplete'),
    path('admins-beneficiaire/autocomplete/', AdminAutocomplete.as_view(), name='administration_beneficiaire_autocomplete'),
    path('bailleur/autocomplete/', BailleurAutocomplete.as_view(), name='bailleur_autocomplete'),
    path('arrondissement/autocomplete/', ArrondissementAutocomplete.as_view(), name='arrondissement_autocomplete'),
    path('agent/autocomplete/', AgentAutocomplete.as_view(), name='agent_autocomplete'),

    # contrat urls
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    path("contrat/print/<int:pk>/", ContratView.print_contrat, name='contrat_print'),
    path("contrat/delete/<int:pk>/", ContratDeleteView.as_view(), name='contrat_delete'),
    path("contrat/update/<int:pk>/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat_update'),
    path("structures/", views.get_structures, name='get_structures'),
    path("arrondissement/", views.get_localisation_datas, name='get_localisation_datas'),

    # consultation :
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),

    # Statistiques :
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),

    # collecte :
    path("collecte/list/", CollecteView.as_view(template_name="baux/collecte_list.html"), name='collecte_list'),
    path("collecte/create", collecte_create, name='collecte_create'),
    path("collecte/print/<int:pk>/", CollecteView.print, name='collecte_print'),
    path("collecte/printfiche/<int:pk>/", CollecteView.printfiche, name='collecte_printfiche'),
    path("collecte/delete/<int:pk>/", CollecteDeleteView.as_view(), name='collecte_delete'),
    path("collecte/update/<int:pk>/", CollecteView.as_view(template_name="baux/collecte.html"), name='collecte_update'),
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    path("add-choice/", dynamic_choice_views.add_dynamic_choice, name="add_dynamic_choice"),

    # fiche collecte new approach
    path("collecte/add/", FicheCollecteFormView.as_view(), name="fiche_collecte_form"),
    path('collecte/<int:fiche_id>/edit/', FicheEditView.as_view(), name='edit_fiche'),

    # api endpoints
    path('api/search-agents/', AgentNomSelect2().get, name='api_agents'),
    path('api/search-matricule-agents/', AgentMatriculeSelect2().get, name='api_matricules_agents'),
    path("api/get-agent-name/", api_fiche_views.get_agent_name, name='get_agent_name'),
    path("api/get-pays/", PaysSelect2().get, name='api_pays'),
    path("api/get-regions/", RegionSelect2().get, name="api_regions"),
    path("api/get-departement/", DepartementSelect2().get, name="api_departement"),
    path("api/get-arrondissement/", ArrondissemntSelect2().get, name="api_arrondissement"),
    path("api/get-administrations/", AdminisrationsSelect2().get, name="api_adminisration"),
    path("api/get-structures/", StructuresSelect2().get, name="api_structures"),
    path("api/get-bailleurs/", BailleursSelect2().get, name="api_bailleurs"),
    path("api/get-banques/", BanquesSelect2().get, name="api_banques"),
    path("api/get-exercices/", ExercicesSelect2.as_view(), name="api_exercices"),
    # api immeubles
    path("api/get-immeubles/", ImmeublesSelect2().get, name="api_immeubles"),
    path("api/get-immeubles/<int:immeuble_id>/", api_immeuble_views.get_immeuble_data, name="get_immeuble_data"),
    # api fiches
    path('api/fiches/numero/', api_fiche_views.generate_fiche_collecte_number, name='generate_fiche_collecte_number'),
    path('api/fiches/create/', api_fiche_views.create_fiche_collecte, name='create_fiche_collecte'),
    path('api/fiches/<int:fiche_id>/', api_fiche_views.get_fiche_collecte, name='get_fiche_collecte'),
    path('api/fiches/<int:fiche_id>/update/', api_fiche_views.update_fiche_collecte, name='update_fiche_collecte'),
    path('api/bailleur/create/', api_bailleur_views.create_bailleur, name='create_bailleur'),
]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static('/uploads/', document_root=os.path.join(settings.BASE_DIR, 'uploads'))
