from django.urls import path

from .views import (
    compte_adm_depense,
    display_compte_depense,
    display_compte_recette,
    EntiteList,
    budget_execution_list,
    saisie_compte_depense,
    saisie_compte_recette,
    upd_compte_depense,
    upd_compte_recette,
	dashboard,
    controle_compte_adm,
    controle_compte_gestion,
    validate_compte_adm,
    validate_compte_gestion,
)

from .api_views import BudgetArticleApiView, BudgetArticleMvtDepenseApiView

urlpatterns = [
    #path('infocentre/', EntiteList.as_view(), name='infocentre-entites'),
    path('infocentre/entites/', EntiteList.as_view(), name='infocentre-entites'),
    path('infocentre/budget_execution_list/<int:budget_entity_id>', budget_execution_list, name='infocentre-executions'),
    
    path('infocentre/display_compte_depense/<int:type_compte>/<int:execution_id>', display_compte_depense, name="infocentre-display-compte-depense"),
    path('infocentre/display_compte_recette/<int:type_compte>/<int:execution_id>', display_compte_recette, name="infocentre-display-compte-recette"),
    
    path('infocentre/saisie_compte_adm_depense/<int:execution_id>', compte_adm_depense, name="infocentre-saisie-compte-adm-depense"),
    
    path('infocentre/saisie_compte_depense/<int:type_compte>/<int:execution_id>', saisie_compte_depense, name="infocentre-saisie-compte-depense"),
    path('infocentre/saisie_compte_recette/<int:type_compte>/<int:execution_id>', saisie_compte_recette, name="infocentre-saisie-compte-recette"),
    
    path('infocentre/upd_compte_depense/<int:type_compte>/<int:execution_mvt_id>', upd_compte_depense, name="infocentre-upd-compte-depense"),
    path('infocentre/upd_compte_recette/<int:type_compte>/<int:execution_mvt_id>', upd_compte_recette, name="infocentre-upd-compte-recette"),

    path('infocentre/controle_compte_adm/<int:execution_id>', controle_compte_adm, name="infocentre-controle-ca"),
    path('infocentre/controle_compte_gestion/<int:execution_id>', controle_compte_gestion, name="infocentre-controle-cg"),
    path('infocentre/validate_compte_adm/<int:execution_id>', validate_compte_adm, name="infocentre-validate-ca"),
    path('infocentre/validate_compte_gestion/<int:execution_id>', validate_compte_gestion, name="infocentre-validate-cg"),
    
    path('infocentre/', dashboard, name='infocentre-dashboard'),

    path('infocentre/api/<str:compte>', BudgetArticleApiView.as_view()),
    path('infocentre/api/<int:article_id>/<int:execution_id>', BudgetArticleMvtDepenseApiView.as_view()),
]