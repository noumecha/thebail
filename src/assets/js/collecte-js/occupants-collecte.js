// Gestion des occupants logements
(function () {
  let rowCounter = 0;
  const $tbody = $('#occupants-logements-tbody');
  const $table = $('#occupants-logements-table');

  // Template de ligne (à adapter selon votre structure)
  function getRowTemplate(rowId) {
    return `
      <tr class="occupant-row" data-row-id="${rowId}">
        <td class="p-0">
          <input type="text"
            class="form-control form-control-sm occupant-field"
            name="occupant_${rowId}_nom_prenom"
            placeholder="Nom & Prénoms"
            data-field="nom_prenom">
        </td>
        <td class="p-0">
          <select style="width: 100% !important;" class="form-select form-select-sm select2-ajax occupant-field"
            name="occupant_${rowId}_administration"
            data-ajax-url="/api/get-administrations/"
            data-ajax-placeholder="Rechercher une administration..."
            data-field="administration">
          </select>
        </td>
        <td class="p-0">
          <input type="text"
            class="form-control form-control-sm occupant-field"
            name="occupant_${rowId}_fonction"
            placeholder="Fonction"
            data-field="fonction">
        </td>
        <td class="p-0">
          <input type="text"
            class="form-control form-control-sm occupant-field"
            name="occupant_${rowId}_matricule"
            placeholder="Matricule"
            data-field="matricule">
        </td>
        <td class="p-0">
          <input type="text"
            class="form-control form-control-sm occupant-field"
            name="occupant_${rowId}_reference"
            placeholder="Référence"
            data-field="reference">
        </td>
        <td class="p-0">
          <input type="date"
            class="form-control form-control-sm occupant-field"
            name="occupant_${rowId}_date"
            data-field="date">
        </td>
        <td class="p-0">
          <div class="btn-group btn-group-sm" role="group">
            <button type="button" class="btn btn-outline-danger delete-occupant-row" title="Supprimer">
              <i class="bx bx-trash"></i>
            </button>
          </div>
        </td>
      </tr>
    `;
  }

  // Initialiser Select2 pour une ligne
  function initSelect2ForRow($row) {
    $row.find('.select2-ajax').each(function () {
      const $select = $(this);
      const ajaxUrl = $select.data('ajax-url');
      const placeholder = $select.data('ajax-placeholder');

      $select.select2({
        ajax: {
          url: ajaxUrl,
          dataType: 'json',
          delay: 250,
          data: function (params) {
            return {
              q: params.term,
              page: params.page || 1
            };
          },
          processResults: function (data) {
            return {
              results: data.results,
              pagination: {
                more: data.pagination.more
              }
            };
          },
          cache: true
        },
        placeholder: placeholder || 'Rechercher...',
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
        },
        width: '100%'
        //dropdownParent: $('#occupants-logements-table').closest('.card-body')
      });
    });
  }

  // Ajouter une nouvelle ligne
  function addNewRow() {
    rowCounter++;
    const $newRow = $(getRowTemplate(rowCounter));
    $tbody.append($newRow);

    // Initialiser Select2 pour cette ligne
    initSelect2ForRow($newRow);

    // Focus sur le premier champ
    $newRow.find('input:first').focus();

    return $newRow;
  }

  // Vérifier si une ligne est complète
  function isRowComplete($row) {
    let isComplete = true;
    $row.find('.occupant-field').each(function () {
      const $field = $(this);
      const value = $field.val();

      // Vérifier si le champ est vide (sauf pour Select2)
      if ($field.hasClass('select2-ajax')) {
        if (!value || value === '') {
          isComplete = false;
        }
      } else {
        if (!value || value.trim() === '') {
          isComplete = false;
        }
      }
    });
    return isComplete;
  }

  // Vérifier s'il existe une ligne vide
  function hasEmptyRow() {
    let hasEmpty = false;
    $tbody.find('.occupant-row').each(function () {
      if (!isRowComplete($(this))) {
        hasEmpty = true;
        return false; // break
      }
    });
    return hasEmpty;
  }

  // Auto-ajout d'une ligne après remplissage
  $tbody.on('change blur', '.occupant-field', function () {
    const $row = $(this).closest('.occupant-row');

    // Si la ligne est complète et qu'il n'y a pas de ligne vide
    if (isRowComplete($row) && !hasEmptyRow()) {
      setTimeout(() => {
        addNewRow();
      }, 300);
    }
  });

  // Bouton d'ajout manuel
  $('#add-occupant-row').on('click', function () {
    addNewRow();
  });

  // Supprimer une ligne
  $tbody.on('click', '.delete-occupant-row', function () {
    const $row = $(this).closest('.occupant-row');
    const rowCount = $tbody.find('.occupant-row').length;

    if (rowCount > 1) {
      // Détruire Select2 avant de supprimer
      $row.find('.select2-ajax').select2('destroy');
      $row.remove();
    } else {
      // Si c'est la dernière ligne, juste vider les champs
      $row.find('.occupant-field').each(function () {
        if ($(this).hasClass('select2-ajax')) {
          $(this).val(null).trigger('change');
        } else {
          $(this).val('');
        }
      });
    }
  });

  // Ajouter la première ligne au chargement
  addNewRow();
})();
