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
});
