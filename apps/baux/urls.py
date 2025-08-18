from django.urls import path
from . import views
from django.contrib import admin
from .views import TypeContratView,CollecteView,HomeView,ConsultationView, BailleurAutocomplete, StructureAutocomplete, AdminAutocomplete, LocataireView,StatsView, BailleurView, LocalisationView, ContratView, ImmeubleView, OccupantsView,Non_MandatementView,AvenantsView,ContratDeleteView,ContratUpdateView
from .forms import LocatairesForm,AccessoiresForm, BailleursForm

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
    *get_crud_urls(Non_MandatementView, "non_mandatement/non_mandatements", "non_mandatement"),
    *get_crud_urls(LocalisationView, "localisation/localisations", "localisation"),
    *get_crud_urls(OccupantsView, "occupant/occupants", "occupant"),
    *get_crud_urls(AvenantsView, "avenant/avenants", "avenant"),
    # 
    path("", HomeView.as_view(template_name="baux/index.html"), name='Index'),
    # bailleur routes 
    path('bailleur-partial-form/', views.bailleur_partial_form_view, name='bailleur_partial_form'),
    # locataire routes
    #path('locataire-partial-form/', views._partial_form_view, name='locataire_partial_form'),
    path('immeuble-partial-form/', views.immeuble_partial_form_view, name='immeuble_partial_form'), # for modal purpose
    path("Menuimmeuble/add/", views.Menuimmeuble, name='Menuimmeuble'),
    # autocomplet on contrat form
    path('structure/autocomplete/', StructureAutocomplete.as_view(), name='structure_autocomplete'),
    path('admin/autocomplete/', AdminAutocomplete.as_view(), name='admins_autocomplete'),
    path('bailleur/autocomplete/', BailleurAutocomplete.as_view(), name='bailleur_autocomplete'),
    # contrat urls
    path("contrat/add/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat'),
    path("contrat/list/", ContratView.as_view(template_name="baux/contrat_list.html"), name='contrat_list'),
    path("contrat/types/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_list'),
    path("contrat/update/<int:pk>/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_update'),
    path("contrat/delete/<int:pk>/", TypeContratView.as_view(template_name="baux/type_contrat_list.html"), name='type_contrat_delete'),
    path("contrat/types/form/", views.typecontrat_form_view, name='type_contrat_form'),  # for modal purpose
    path("structures/", views.get_structures, name='get_structures'),  # for filtering structures based on administration <int:administration_id>
    #path("contrat/print/<int:pk>/", ContratView.as_view(template_name="baux/docs/contrat_doc.html"), name='contrat_print'),
    path("contrat/print/<int:pk>/", ContratView.print_contrat, name='contrat_print'),
    path("contrat/delete/<int:pk>/", ContratDeleteView.as_view(), name='contrat_delete'),
    path("contrat/update/<int:pk>/", ContratView.as_view(template_name="baux/contrat.html"), name='contrat_update'),
    # consultation : 
    path("consultation", ConsultationView.as_view(template_name="baux/consultation.html"), name='consultation'),
    # Statistiques : 
    path("stats", StatsView.as_view(template_name="baux/stats.html"), name='stats'),
    # collecte : 
    path('collecte/add/', CollecteView.as_view([LocatairesForm,AccessoiresForm, BailleursForm]), name='collecte'),
]
