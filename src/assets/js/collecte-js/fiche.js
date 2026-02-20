$(function () {
  // gestion dynamique avec pour les modals et les éléments de types list avec checkbox
  const ajax_modal_objects = [
    {
      modalId: '#addTypeContratModal',
      formContainerId: '#typecontrat-form-content',
      formId: '#typecontratForm',
      fetchUrl: '/type-contrat-partial-form/',
      selectItemId: '#id_TypeContrat'
    },
    {
      modalId: '#addRevetementInterieureModal',
      formContainerId: '#revetementint-form-content',
      formId: '#revetementintForm',
      fetchUrl: '/revetement-int-partial-form/',
      selectItemId: '#id_immeubles-0-Revetement_interieure'
    },
    {
      modalId: '#addRevetementExterieureModal',
      formContainerId: '#revetementext-form-content',
      formId: '#revetementextForm',
      fetchUrl: '/revetement-ext-partial-form/',
      selectItemId: '#id_immeubles-0-Revetement_exterieure'
    },
    {
      modalId: '#addExerciceModal',
      formContainerId: '#exercice-form-content',
      formId: '#exerciceForm',
      fetchUrl: '/exercice-partial-form/',
      selectItemId: '#id_non_mandatements-0-Exercice'
    },
    {
      modalId: '#addBailleurModal',
      formContainerId: '#bailleur-form-content',
      formId: '#bailleurForm',
      fetchUrl: '/bailleur-partial-form/',
      selectItemId: '#id_Bailleur'
    },
    {
      modalId: '#addPieceModal',
      formContainerId: '#piece-form-content',
      formId: '#pieceForm',
      fetchUrl: '/piece-collecte-partial-form/',
      selectItemId: '#pieces-collecte-container'
    }
  ];
  ajax_modal_objects.forEach(obj => {
    ajaxModal(obj.modalId, obj.formContainerId, obj.formId, obj.fetchUrl, obj.selectItemId);
  });

  // elements and pieces adding
  const add_to_list_object = [
    {
      list_container: '#pieces-collecte-container',
      list_input: 'piece-collecte-input',
      list_btn: 'add-piece-btn',
      list_url: '/piece-collecte-partial-form/'
    },
    {
      list_container: '#elements-immeuble-container',
      list_input: 'element-immeuble-input',
      list_btn: 'add-element-btn',
      list_url: '/element-description-partial-form/'
    }
  ];
  add_to_list_object.forEach(obj => {
    addElementToList(obj.list_container, obj.list_input, obj.list_btn, obj.list_url);
  });

  initSelect2Ajax();

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
  const dynamic_choices_list_objects = [
    {
      listId: 'type_construction_id',
      hiddenId: 'construction_choice_hidden',
      newInputId: 'new_construction_input',
      formWrapper: 'new_construction_wrapper',
      addButtonId: 'add_construction_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'type_location_id',
      hiddenId: 'type_location_choice_hidden',
      newInputId: 'new_type_location_input',
      formWrapper: 'new_type_location_wrapper',
      addButtonId: 'add_type_location_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'statut_batisse_id',
      hiddenId: 'statut_choice_hidden',
      newInputId: 'new_statut_input',
      formWrapper: 'new_statut_wrapper',
      addButtonId: 'add_statut_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'revetement_int_id',
      hiddenId: 'revetementinterieure_choice_hidden',
      newInputId: 'new_revetementinterieure_input',
      formWrapper: 'new_revetementinterieure_wrapper',
      addButtonId: 'add_revetementinterieure_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'revetement_ext_id',
      hiddenId: 'revetementexterieure_choice_hidden',
      newInputId: 'new_revetementexterieure_input',
      formWrapper: 'new_revetementexterieure_wrapper',
      addButtonId: 'add_revetementexterieure_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'TypeContrat',
      hiddenId: 'typecontrat_choice_hidden',
      newInputId: 'new_typecontrat_input',
      formWrapper: 'new_typecontrat_wrapper',
      addButtonId: 'add_typecontrat_btn',
      ajaxUrl: '/add-choice/'
    },
    {
      listId: 'Periodicite_Reglement_id',
      hiddenId: 'periodicitereglement_choice_hidden',
      newInputId: 'new_periodicitereglement_input',
      formWrapper: 'new_periodicitereglement_wrapper',
      addButtonId: 'add_periodicitereglement_btn',
      ajaxUrl: '/add-choice/'
    }
  ];
  dynamic_choices_list_objects.forEach(obj => {
    initDynamicChoiceList(obj.listId, obj.hiddenId, obj.newInputId, obj.formWrapper, obj.addButtonId, obj.ajaxUrl);
  });

  // gérer les checkbox oui/non des éléments de type oui/non
  const object_to_toggle = [
    { listId: 'Type_personne', hiddenId: 'types_personnes_choice' },
    { listId: 'Statut_bailleur', hiddenId: 'statut_bailleur_choice' },
    { listId: 'Role_bailleur', hideenId: 'role_bailleur_choice' },
    { listId: 'Existence_visa_budgétaire', hiddenId: null },
    { listId: 'tacite_reconduction', hiddenId: null },
    { listId: 'Existence_avenant', hiddenId: null },
    { listId: 'statut_visa_budgetaire_avenant_1', hiddenId: null },
    { listId: 'statut_visa_budgetaire_avenant_2', hiddenId: null },
    { listId: 'type_construction_id', hiddenId: null },
    { listId: 'TypeContrat', hiddenId: null },
    { listId: 'Periodicite_Reglement_id', hiddenId: null },
    { listId: 'type_location_id', hiddenId: null },
    { listId: 'statut_batisse_id', hiddenId: null },
    { listId: 'revetement_int_id', hiddenId: null },
    { listId: 'revetement_ext_id', hiddenId: null },
    { listId: 'Tacite_reconduction_contrat', hiddenId: null }
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
  const isStatutChecked = $('#Statut_bailleur .dynamic-check').is(':checked');
  $('#Role_bailleur .dynamic-check').prop('disabled', !isStatutChecked);
  $('#Statut_bailleur').on('change', '.dynamic-check', function () {
    const isChecked = $(this).is(':checked');
    $('#Role_bailleur .dynamic-check').prop('disabled', !isChecked);
    if (!isChecked) {
      $('#Role_bailleur .dynamic-check').prop('checked', false).trigger('change');
    }
  });
});
