// Gestionnaire générique de tableaux dynamiques
function DynamicTableManager(config) {
  const {
    tbodyId,
    addButtonId,
    tableId,
    rowPrefix,
    fields,
    autoAdd = true,
    minRows = 1,
    showRowNumber = false,
    customTemplate = null, // ✅ Template personnalisé
    onRowCreated = null // ✅ Callback après création de ligne
  } = config;

  let rowCounter = 0;
  const $tbody = $('#' + tbodyId);
  const $table = $('#' + tableId);
  const $addButton = $('#' + addButtonId);

  // Générer le template de ligne dynamiquement
  function getRowTemplate(rowId) {
    // ✅ Utiliser le template personnalisé si fourni
    if (customTemplate) {
      return customTemplate(rowId, rowPrefix);
    }

    let rowHtml = `<tr class="dynamic-row" data-row-id="${rowId}">`;

    if (showRowNumber) {
      rowHtml += `<td class="text-center p-0 row-number">${rowId}</td>`;
    }

    fields.forEach(field => {
      rowHtml += `<td class="p-0">`;

      if (field.type === 'select2') {
        rowHtml += `
          <select style="width: 100% !important;"
            class="form-select form-select-sm select2-ajax dynamic-field"
            name="${rowPrefix}_${rowId}_${field.name}"
            data-ajax-url="${field.ajaxUrl}"
            data-ajax-placeholder="${field.placeholder || 'Rechercher...'}"
            data-field="${field.name}">
          </select>
        `;
      } else if (field.type === 'checkbox-group') {
        // ✅ Support pour groupe de checkboxes
        rowHtml += `<div class="d-flex gap-1 checkbox-group" data-field="${field.name}">`;
        field.options.forEach((option, index) => {
          rowHtml += `
            <input type="checkbox"
              class="form-check-input month-checkbox"
              name="${rowPrefix}_${rowId}_${field.name}_${index}"
              value="${option.value}"
              data-month="${option.value}">
          `;
        });
        rowHtml += `</div>`;
      } else if (field.type === 'text' || field.type === 'date' || field.type === 'number') {
        const readonly = field.readonly ? 'readonly' : '';
        const extraClass = field.className || '';
        rowHtml += `
          <input type="${field.type}"
            class="form-control form-control-sm dynamic-field ${extraClass}"
            name="${rowPrefix}_${rowId}_${field.name}"
            placeholder="${field.placeholder || ''}"
            data-field="${field.name}"
            ${readonly}>
        `;
      }

      rowHtml += `</td>`;
    });

    // Colonne Actions
    rowHtml += `
      <td class="p-0">
        <div class="btn-group btn-group-sm" role="group">
          <button type="button" class="btn btn-outline-danger delete-row" title="Supprimer">
            <i class="bx bx-trash"></i>
          </button>
        </div>
      </td>
    </tr>`;

    return rowHtml;
  }

  function updateRowNumbers() {
    if (showRowNumber) {
      $tbody.find('.dynamic-row').each(function (index) {
        $(this)
          .find('.row-number')
          .text(index + 1);
      });
    }
  }

  function initSelect2ForRow($row) {
    $row.find('.select2-ajax').each(function () {
      const $select = $(this);

      if ($select.hasClass('select2-hidden-accessible')) {
        return;
      }

      const ajaxUrl = $select.data('ajax-url');
      const placeholder = $select.data('ajax-placeholder');

      try {
        $select.select2({
          ajax: {
            url: ajaxUrl,
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return { q: params.term, page: params.page || 1 };
            },
            processResults: function (data) {
              return {
                results: data.results,
                pagination: { more: data.pagination.more }
              };
            },
            cache: true
          },
          placeholder: placeholder || 'Rechercher...',
          minimumInputLength: 2,
          language: {
            inputTooShort: () => 'Veuillez saisir au moins 2 caractères',
            searching: () => 'Recherche en cours...',
            noResults: () => 'Aucun résultat trouvé'
          },
          width: '100%'
        });
      } catch (error) {
        console.error('Erreur Select2:', error);
      }
    });
  }

  function addNewRow() {
    rowCounter++;
    const $newRow = $(getRowTemplate(rowCounter));
    $tbody.append($newRow);

    updateRowNumbers();

    setTimeout(() => {
      initSelect2ForRow($newRow);

      // ✅ Appeler le callback personnalisé
      if (onRowCreated) {
        onRowCreated($newRow, rowCounter);
      }

      $newRow.find('input:first, select:first').focus();
    }, 100);

    return $newRow;
  }

  function isRowComplete($row) {
    let isComplete = true;
    $row.find('.dynamic-field').each(function () {
      const $field = $(this);
      const value = $field.val();

      if (!value || value.trim() === '') {
        isComplete = false;
        return false;
      }
    });
    return isComplete;
  }

  function hasEmptyRow() {
    let hasEmpty = false;
    $tbody.find('.dynamic-row').each(function () {
      if (!isRowComplete($(this))) {
        hasEmpty = true;
        return false;
      }
    });
    return hasEmpty;
  }

  if (autoAdd) {
    $tbody.on('change blur', '.dynamic-field', function () {
      const $row = $(this).closest('.dynamic-row');

      if (isRowComplete($row) && !hasEmptyRow()) {
        setTimeout(() => addNewRow(), 100);
      }
    });
  }

  $addButton.on('click', function () {
    addNewRow();
  });

  $tbody.on('click', '.delete-row', function () {
    const $row = $(this).closest('.dynamic-row');
    const rowCount = $tbody.find('.dynamic-row').length;

    if (rowCount > minRows) {
      $row.find('.select2-ajax').each(function () {
        if ($(this).hasClass('select2-hidden-accessible')) {
          $(this).select2('destroy');
        }
      });
      $row.remove();
      updateRowNumbers();
    } else {
      $row.find('.dynamic-field').each(function () {
        if ($(this).hasClass('select2-ajax')) {
          $(this).val(null).trigger('change');
        } else {
          $(this).val('');
        }
      });
    }
  });

  this.collectData = function () {
    const data = [];
    $tbody.find('.dynamic-row').each(function () {
      const $row = $(this);
      const rowId = $row.data('row-id');
      const rowData = {};

      fields.forEach(field => {
        const value = $row.find(`[name="${rowPrefix}_${rowId}_${field.name}"]`).val();
        rowData[field.name] = value;
      });

      if (Object.values(rowData).some(v => v && v.trim() !== '')) {
        data.push(rowData);
      }
    });
    return data;
  };

  addNewRow();
}

// utilisation :
$(function () {
  // tableaux dynamique d'ajouts d'éléments
  // Initialiser le tableau des ayants droit (avec numérotation)
  const ayantsDroitManager = new DynamicTableManager({
    tbodyId: 'ayants-droit-tbody',
    addButtonId: 'add-ayant-droit-row',
    tableId: 'ayants-droit-table',
    rowPrefix: 'ayant_droit',
    autoAdd: true,
    minRows: 1,
    showRowNumber: true, // ✅ Activer la numérotation
    fields: [
      { name: 'nom_prenom', type: 'text', placeholder: 'Nom & Prénoms' },
      { name: 'contact', type: 'text', placeholder: 'Contact' },
      { name: 'reference_grosse', type: 'text', placeholder: 'Référence Grosse' },
      { name: 'date_delivrance_grosse', type: 'date' },
      { name: 'reference_certificat', type: 'text', placeholder: 'Référence Certificat' },
      { name: 'date_delivrance_certificat', type: 'date' }
    ]
  });

  const logementsManager = new DynamicTableManager({
    tbodyId: 'occupants-logements-tbody',
    addButtonId: 'add-occupant-logement-row',
    tableId: 'occupants-logements-table',
    rowPrefix: 'occupant_logement',
    autoAdd: true,
    minRows: 1,
    showRowNumber: false, // ✅ Pas de numérotation
    fields: [
      { name: 'nom_prenom', type: 'text', placeholder: 'Nom & Prénoms' },
      {
        name: 'administration',
        type: 'select2',
        ajaxUrl: '/api/get-administrations/',
        placeholder: 'Rechercher une administration...'
      },
      { name: 'fonction', type: 'text', placeholder: 'Fonction' },
      { name: 'matricule', type: 'text', placeholder: 'Matricule' },
      { name: 'reference', type: 'text', placeholder: 'Référence' },
      { name: 'date', type: 'date' }
    ]
  });

  const bureauxManager = new DynamicTableManager({
    tbodyId: 'occupants-bureaux-tbody',
    addButtonId: 'add-occupant-bureau-row',
    tableId: 'occupants-bureaux-table',
    rowPrefix: 'occupant_bureau',
    autoAdd: true,
    minRows: 1,
    showRowNumber: false, // ✅ Pas de numérotation
    fields: [
      { name: 'service', type: 'select2', ajaxUrl: '/api/get-structures/', placeholder: 'Rechercher un service...' },
      {
        name: 'administration',
        type: 'select2',
        ajaxUrl: '/api/get-administrations/',
        placeholder: 'Rechercher une administration...'
      },
      { name: 'fonction_responsable', type: 'text', placeholder: 'Fonction du responsable' },
      { name: 'reference_acte', type: 'text', placeholder: 'Référence' },
      { name: 'date_signature', type: 'date' }
    ]
  });

  // non-mandatement management
  // Template personnalisé pour non-mandatement
  function getNonMandatementTemplate(rowId, rowPrefix) {
    const months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];

    return `
    <tr class="dynamic-row" data-row-id="${rowId}">
      <td class="p-0">
        <select style="width: 100% !important;"
          class="form-select form-select-sm select2-ajax dynamic-field"
          name="${rowPrefix}_${rowId}_exercice"
          data-ajax-url="/api/get-exercices/"
          data-ajax-placeholder="Rechercher un exercice..."
          data-field="exercice">
        </select>
      </td>
      <td class="p-0">
        <input type="number"
          class="form-control form-control-sm dynamic-field loyer-mensuel"
          name="${rowPrefix}_${rowId}_loyer_mensuel"
          placeholder="Loyer mensuel"
          data-field="loyer_mensuel"
          min="0">
      </td>
      <td class="p-0">
        <input type="text"
          class="form-control form-control-sm dynamic-field"
          name="${rowPrefix}_${rowId}_reference"
          placeholder="Référence"
          data-field="reference">
      </td>
      <td class="p-0">
        <input type="date"
          class="form-control form-control-sm dynamic-field"
          name="${rowPrefix}_${rowId}_date_signature"
          data-field="date_signature">
      </td>
      ${months
        .map(
          (month, index) => `
        <td class="p-0 text-center">
          <input type="checkbox"
            class="form-check-input month-checkbox"
            name="${rowPrefix}_${rowId}_mois_${index + 1}"
            value="${index + 1}"
            data-month="${month}">
        </td>
      `
        )
        .join('')}
      <td class="p-0">
        <input type="number"
          class="form-control form-control-sm montant-total"
          name="${rowPrefix}_${rowId}_montant_total"
          placeholder="Montant total"
          data-field="montant_total"
          readonly>
      </td>
      <td class="p-0">
        <input type="text"
          class="form-control form-control-sm dynamic-field"
          name="${rowPrefix}_${rowId}_visa"
          placeholder="Visa"
          data-field="visa">
      </td>
      <td class="p-0">
        <input type="text"
          class="form-control form-control-sm dynamic-field"
          name="${rowPrefix}_${rowId}_reference_contrat"
          placeholder="Référence contrat"
          data-field="reference_contrat">
      </td>
      <td class="p-0">
        <div class="btn-group btn-group-sm" role="group">
          <button type="button" class="btn btn-outline-danger delete-row" title="Supprimer">
            <i class="bx bx-trash"></i>
          </button>
        </div>
      </td>
    </tr>
  `;
  }

  // Fonction pour calculer le montant total
  function calculateMontantTotal($row) {
    const loyerMensuel = parseFloat($row.find('.loyer-mensuel').val()) || 0;
    const checkedMonths = $row.find('.month-checkbox:checked').length;
    const montantTotal = loyerMensuel * checkedMonths;

    $row.find('.montant-total').val(montantTotal.toFixed(2));
  }

  // Initialiser le tableau Non-Mandatement
  const nonMandatementManager = new DynamicTableManager({
    tbodyId: 'nonmandatement-collecte-tbody',
    addButtonId: 'add-nonmandatement-row',
    tableId: 'nonmandatement-collecte-table',
    rowPrefix: 'nonmandatement',
    autoAdd: false, // Désactiver l'auto-ajout pour ce tableau complexe
    minRows: 1,
    showRowNumber: false,
    customTemplate: getNonMandatementTemplate,
    onRowCreated: function ($row, rowId) {
      // ✅ Attacher les événements de calcul après création de ligne

      // Calculer quand le loyer mensuel change
      $row.find('.loyer-mensuel').on('input change', function () {
        calculateMontantTotal($row);
      });

      // Calculer quand on coche/décoche un mois
      $row.find('.month-checkbox').on('change', function () {
        calculateMontantTotal($row);
      });
    },
    fields: [] // Pas besoin car on utilise customTemplate
  });

  // Attacher les événements sur le tbody pour les lignes existantes et futures
  $('#nonmandatement-collecte-tbody').on('input change', '.loyer-mensuel', function () {
    const $row = $(this).closest('.dynamic-row');
    calculateMontantTotal($row);
  });

  $('#nonmandatement-collecte-tbody').on('change', '.month-checkbox', function () {
    const $row = $(this).closest('.dynamic-row');
    calculateMontantTotal($row);
  });
});
