import { FormUtils } from './modules/form-utils.js';
import { bindStatutRoleDependency } from './modules/dependencies.js';
$(function () {
  // elements and pieces adding
  const add_to_list_object = [
    {
      list_container: '#pieces-collecte-container',
      list_input: 'pieces-collecte-container-piece-collecte-input',
      list_btn: 'pieces-collecte-container-add-piece-btn',
      list_url: '/piece-collecte-partial-form/'
    },
    {
      list_container: '#main-elements-immeuble-container',
      list_input: 'main-elements-immeuble-container-element-immeuble-input',
      list_btn: 'main-elements-immeuble-container-add-element-btn',
      list_url: '/element-description-partial-form/'
    }
  ];
  add_to_list_object.forEach(obj => {
    FormUtils.addElementToList(obj.list_container, obj.list_input, obj.list_btn, obj.list_url);
  });
  // init select 2 on form
  FormUtils.initSelect2Ajax($('#ficheCollecteForm'));

  // maj du champ responsable de collecte à partir du champ matricule du responsable
  $(document).on('change', '#matricule_responsable_collecte', function () {
    let matricule = $(this).val();
    if (matricule) {
      $.ajax({
        url: '/api/get-agent-name/',
        data: { matricule_agent: matricule },
        success: function (data) {
          if (data.success) {
            let agentName = data.agent;
            let agentId = matricule;
            $('#responsable_collecte').val(agentId).trigger('change');
            let $select = $('#responsable_collecte');
            let $option = $select.find('option[value="' + agentId + '"]');
            if ($option.length) {
              $option.text(agentName);
            } else {
              $select.append(new Option(agentName, agentId, true, true));
              $select.trigger('change');
            }
          }
        },
        error: function (xhr, status, error) {
          console.error('Error getting Agent :', error);
        }
      });
    }
  });

  // gestion des éléments dynamique [elements de type list avec checkbox + éléments de description]
  // id="{{ list_id }}-{{ add_btn_id }}"
  const dynamic_choices_list_objects = [
    {
      listId: 'main_type_construction_id',
      hiddenId: 'main_type_construction_id-construction_choice_hidden',
      newInputId: 'main_type_construction_id-new_construction_input',
      formWrapper: 'main_type_construction_id-new_construction_wrapper',
      addButtonId: 'main_type_construction_id-add_construction_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'main_type_location_id',
      hiddenId: 'main_type_construction_id-type_location_choice_hidden',
      newInputId: 'main_type_construction_id-new_type_location_input',
      formWrapper: 'main_type_construction_id-new_type_location_wrapper',
      addButtonId: 'main_type_construction_id-add_type_location_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'main_statut_batisse_id',
      hiddenId: 'main_type_construction_id-statut_choice_hidden',
      newInputId: 'main_type_construction_id-new_statut_input',
      formWrapper: 'main_type_construction_id-new_statut_wrapper',
      addButtonId: 'main_type_construction_id-add_statut_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'main_revetement_int_id',
      hiddenId: 'main_type_construction_id-revetementinterieure_choice_hidden',
      newInputId: 'main_type_construction_id-new_revetementinterieure_input',
      formWrapper: 'main_type_construction_id-new_revetementinterieure_wrapper',
      addButtonId: 'main_type_construction_id-add_revetementinterieure_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'main_revetement_ext_id',
      hiddenId: 'main_type_construction_id-revetementexterieure_choice_hidden',
      newInputId: 'main_type_construction_id-new_revetementexterieure_input',
      formWrapper: 'main_type_construction_id-new_revetementexterieure_wrapper',
      addButtonId: 'main_type_construction_id-add_revetementexterieure_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'TypeContrat',
      hiddenId: 'TypeContrat-typecontrat_choice_hidden',
      newInputId: 'TypeContrat-new_typecontrat_input',
      formWrapper: 'TypeContrat-new_typecontrat_wrapper',
      addButtonId: 'TypeContrat-add_typecontrat_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'Periodicite_Reglement_id',
      hiddenId: 'Periodicite_Reglement_id-periodicitereglement_choice_hidden',
      newInputId: 'Periodicite_Reglement_id-new_periodicitereglement_input',
      formWrapper: 'Periodicite_Reglement_id-new_periodicitereglement_wrapper',
      addButtonId: 'Periodicite_Reglement_id-add_periodicitereglement_btn',
      ajaxUrl: '/add-choice/'
    }
  ];
  dynamic_choices_list_objects.forEach(obj => {
    initDynamicChoiceList(obj.listId, obj.hiddenId, obj.newInputId, obj.formWrapper, obj.addButtonId, obj.ajaxUrl);
  });

  // gérer les checkbox oui/non des éléments de type oui/non
  const object_to_toggle = [
    // immeuble :
    { listId: 'main_type_construction_id', hiddenId: null },
    { listId: 'main_type_location_id', hiddenId: null },
    { listId: 'main_statut_batisse_id', hiddenId: null },
    { listId: 'main_revetement_int_id', hiddenId: null },
    { listId: 'main_revetement_ext_id', hiddenId: null },
    // contrat :
    { listId: 'Existence_visa_budgétaire', hiddenId: null },
    { listId: 'tacite_reconduction', hiddenId: null },
    { listId: 'Existence_avenant', hiddenId: null },
    { listId: 'statut_visa_budgetaire_avenant_1', hiddenId: null },
    { listId: 'statut_visa_budgetaire_avenant_2', hiddenId: null },
    { listId: 'TypeContrat', hiddenId: null },
    { listId: 'Periodicite_Reglement_id', hiddenId: null },
    { listId: 'Tacite_reconduction_contrat', hiddenId: null },
    // bailleur element :
    { listId: 'main_Type_personne', hiddenId: 'main_types_personnes_choice' },
    { listId: 'main_Statut_bailleur', hiddenId: 'main_statut_bailleur_choice' },
    { listId: 'main_Role_bailleur', hiddenId: 'main_role_bailleur_choice' }
  ];
  object_to_toggle.forEach(obj => {
    $('#' + obj.listId).on('change', '.dynamic-check', function () {
      toggleCheck({
        listId: obj.listId,
        checkbox: this,
        dynamicCheckClass: 'dynamic-check',
        dynamicOptionClass: 'dynamic-option',
        dynamicInputClass: 'dynamic-x-input',
        hiddenId: obj.hiddenId
      });
    });
  });

  // disabled an enable Role_bailleur base on Statut_bailleur checked or no
  // on init check directly if statut_bailleur is checked
  bindStatutRoleDependency('#main_Statut_bailleur', '#main_Role_bailleur');
});
