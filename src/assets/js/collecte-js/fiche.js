function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// fetching agent :
// Dans votre fichier JS principal
$(function () {
  // Initialiser tous les select avec la classe select2-ajax
  $('.select2-ajax').each(function () {
    const $select = $(this);
    const ajaxUrl = $select.data('ajax-url');
    const ajaxPlacholder = $select.data('ajax-placeholder');

    $select.select2({
      ajax: {
        url: ajaxUrl,
        dataType: 'json',
        delay: 250, // Délai avant la recherche (évite trop de requêtes)
        data: function (params) {
          return {
            q: params.term, // Terme de recherche
            page: params.page || 1
          };
        },
        processResults: function (data, params) {
          params.page = params.page || 1;

          return {
            results: data.results,
            pagination: {
              more: data.pagination.more
            }
          };
        },
        cache: true
      },
      placeholder: ajaxPlacholder,
      minimumInputLength: 2,
      language: {
        inputTooShort: function () {
          return 'Veuillez saisir au moins 2 caractères';
        },
        searching: function () {
          return 'Recherche en cours...';
        },
        noResults: function () {
          return 'Aucun résultat trouvé';
        }
      }
    });
  });
  // Gérer les changements
  $(document).on('change', '#matricule_responsable_collecte', function () {
    let matricule = $(this).val();
    if (matricule) {
      $.ajax({
        url: '/api/get-agent-name/',
        data: { matricule_agent: matricule },
        success: function (data) {
          if (data.success) {
            // Mettre à jour le premier select
            let agentName = data.agent;
            let agentId = matricule;

            // Mettre à jour le premier select
            $('#responsable_collecte').val(agentId).trigger('change');

            // Mettre à jour le nom dans le premier select
            let $select = $('#responsable_collecte');
            let $option = $select.find('option[value="' + agentId + '"]');

            if ($option.length) {
              $option.text(agentName);
            } else {
              // Ajouter un nouvel option
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

  // gestion des éléments dynamique pour l'ajout des éléments à la liste dynamique
  initDynamicChoiceList(
    'construction_list',
    'construction_choice_hidden',
    'new_construction_input',
    'add_construction_btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'type_location_list',
    'type_location_choice_hidden',
    'new_type_location_input',
    'add_type_location_btn',
    '/add-choice/'
  );
  initDynamicChoiceList('statut_list', 'statut_choice_hidden', 'new_statut_input', 'add_statut_btn', '/add-choice/');
  initDynamicChoiceList(
    'revetementinterieure_list',
    'revetementinterieure_choice_hidden',
    'new_revetementinterieure_input',
    'add_revetementinterieure_btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'revetementexterieure_list',
    'revetementexterieure_choice_hidden',
    'new_revetementexterieure_input',
    'add_revetementexterieure_btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'typecontrat_list',
    'typecontrat_choice_hidden',
    'new_typecontrat_input',
    'add_typecontrat_btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'periodicitereglement',
    'periodicitereglement_choice_hidden',
    'new_periodicitereglement_input',
    'add_periodicitereglement_btn',
    '/add-choice/'
  );
  // dynamic toogle non object elements
  const object_to_toggle = [
    { listId: 'types_personnes_list', hiddenId: 'types_personnes_choice' },
    { listId: 'statut_bailleur_list', hiddenId: 'statut_bailleur_choice' },
    { listId: 'existance_visa_bugetaire_contrat', hiddenId: null },
    { listId: 'tacite_reconduction', hiddenId: null },
    { listId: 'existence_avenant_contrat', hiddenId: null }
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
  // Gérer TOUS les éléments de description avec un seul événement
  $('#elements-immeuble-container').on('change', '.dynamic-check', function () {
    const $checkbox = $(this);
    const $row = $checkbox.closest('tr');
    const elementId = $row.data('el-id');
    const listId = 'immeuble_element_' + elementId;

    toggleCheck({
      listId: listId,
      checkbox: this,
      dynamicCheckClass: 'dynamic-check',
      dynamicOptionClass: 'dynamic-option',
      dynamicInputClass: 'dynamic-x-input',
      hiddenId: null
    });
  });
});
