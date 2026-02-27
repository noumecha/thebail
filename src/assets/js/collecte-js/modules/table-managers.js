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
    toggleChecker = null, // callback for yes or no choice
    customTemplate = null, // ✅ Template personnalisé
    onRowCreated = null, // ✅ Callback après création de ligne
    customCollectData = null // ✅ Nouveau paramètre
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
          <select style="width: 300px !important;"
            class="form-select form-select-sm select2-ajax dynamic-field"
            name="${rowPrefix}_${rowId}_${field.name}"
            data-ajax-url="${field.ajaxUrl}"
            data-ajax-placeholder="${field.placeholder || 'Rechercher...'}"
            data-field="${field.name}"
            data-ajax-length="2">
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
            ${field.settings || ''}
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

  function addNewRow() {
    rowCounter++;
    const $newRow = $(getRowTemplate(rowCounter));
    $tbody.append($newRow);

    updateRowNumbers();

    setTimeout(() => {
      initSelect2Ajax($newRow, rowPrefix);

      // ✅ Appeler le callback personnalisé
      if (onRowCreated) {
        onRowCreated($newRow, rowCounter);
      }

      if (toggleChecker) {
        toggleChecker(rowCounter);
      }

      $newRow.find('input:first, select:first').focus();
    }, 100);

    return $newRow;
  }

  this.addNewRow = function () {
    return addNewRow();
  };

  this.clearAllRows = function () {
    $tbody.find('.dynamic-row').each(function () {
      const $row = $(this);
      $row.find('.select2-ajax').each(function () {
        if ($(this).hasClass('select2-hidden-accessible')) {
          $(this).select2('destroy');
        }
      });
    });
    $tbody.empty();
    rowCounter = 0;
  };

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

  // Ajouter cette méthode au DynamicTableManager
  this.collectData = function () {
    // utiliser la fonction personnalisée
    if (customCollectData && typeof customCollectData === 'function') {
      return customCollectData();
    }
    const data = [];
    $tbody.find('.dynamic-row').each(function () {
      const $row = $(this);
      const rowId = $row.data('row-id');
      const rowData = {};

      fields.forEach(field => {
        if (field.type === 'checkbox-group') {
          // Pour les checkboxes (mois non-mandatés)
          const checkedValues = [];
          $row.find(`[data-field="${field.name}"]:checked`).each(function () {
            checkedValues.push({
              mois_numero: parseInt($(this).val()),
              statut: true
            });
          });
          rowData[field.name] = checkedValues;
        } else {
          const value = $row.find(`[name="${rowPrefix}_${rowId}_${field.name}"]`).val();
          rowData[field.name] = value;
        }
      });

      // N'ajouter que les lignes avec des données
      const hasData = Object.values(rowData).some(v => {
        if (Array.isArray(v)) return v.length > 0;
        return v && v.toString().trim() !== '';
      });

      if (hasData) {
        data.push(rowData);
      }
    });
    return data;
  };

  addNewRow();
}
