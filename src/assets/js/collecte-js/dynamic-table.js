import { FormUtils } from './modules/form-utils.js';
// exposition des managers
window.TableManagers = window.TableManagers || {};

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
      FormUtils.initSelect2Ajax($newRow, rowPrefix);

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

// appel :
$(function () {
  // tableaux dynamique d'ajouts d'éléments
  // Initialiser le tableau des ayants droit (avec numérotation)
  window.TableManagers.ayantsDroitManager = new DynamicTableManager({
    tbodyId: 'ayants-droit-tbody',
    addButtonId: 'add-ayant-droit-row',
    tableId: 'ayants-droit-table',
    rowPrefix: 'ayant_droit',
    autoAdd: true,
    minRows: 1,
    showRowNumber: true, // ✅ Activer la numérotation
    fields: [
      { name: 'Nom_Prenom_ayant_droit', type: 'text', placeholder: 'Nom & Prénoms' },
      { name: 'Contact_ayant_droit', type: 'text', placeholder: 'Contact' },
      { name: 'Reference_Grosse_ayant_droit', type: 'text', placeholder: 'Référence Grosse' },
      { name: 'Date_delivrance_grosse', type: 'date' },
      { name: 'Reference_certificat_non_appel', type: 'text', placeholder: 'Référence Certificat' },
      { name: 'Date_delivrance_certificat_non_appel', type: 'date' }
    ]
  });

  window.TableManagers.logementsManager = new DynamicTableManager({
    tbodyId: 'occupants-logements-tbody',
    addButtonId: 'add-occupant-logement-row',
    tableId: 'occupants-logements-table',
    rowPrefix: 'occupant_logement',
    autoAdd: true,
    minRows: 1,
    showRowNumber: false, // ✅ Pas de numérotation
    fields: [
      { name: 'Nom_Prenom_occupant_residence', type: 'text', placeholder: 'Nom & Prénoms' },
      {
        name: 'Administration_rattachement',
        type: 'select2',
        ajaxUrl: '/api/get-administrations/',
        placeholder: 'Rechercher une administration...'
      },
      { name: 'Fonction_occupant_residence', type: 'text', placeholder: 'Fonction' },
      { name: 'Matricule_occupant_residence', type: 'text', placeholder: 'Matricule', settings: "maxlength='7'" },
      { name: 'Ref_ActeJuridique_attribution', type: 'text', placeholder: 'Référence' },
      { name: 'Date_Signature_acte_juridique', type: 'date' }
    ]
  });

  window.TableManagers.bureauxManager = new DynamicTableManager({
    tbodyId: 'occupants-bureaux-tbody',
    addButtonId: 'add-occupant-bureau-row',
    tableId: 'occupants-bureaux-table',
    rowPrefix: 'occupant_bureau',
    autoAdd: true,
    minRows: 1,
    showRowNumber: false, // ✅ Pas de numérotation
    fields: [
      {
        name: 'Service_occupant_bureau',
        type: 'select2',
        ajaxUrl: '/api/get-structures/',
        placeholder: 'Rechercher un service...'
      },
      {
        name: 'Administration_correspondante',
        type: 'select2',
        ajaxUrl: '/api/get-administrations/',
        placeholder: 'Rechercher une administration...'
      },
      { name: 'Fonction_occupant_bureau', type: 'text', placeholder: 'Fonction du responsable' },
      { name: 'Ref_ActeJuridique_attribution', type: 'text', placeholder: 'Référence' },
      { name: 'Date_signature_acte_attribution', type: 'date' }
    ]
  });

  // non-mandatement management
  // Template personnalisé pour non-mandatement
  function getNonMandatementTemplate(rowId, rowPrefix) {
    const months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];

    return `
    <tr class="dynamic-row" data-row-id="${rowId}">
      <td class="p-0">
        <select style="width: 150px !important;"
          class="form-select form-select-sm select2-ajax dynamic-field"
          id="${rowPrefix}_${rowId}_exercice"
          name="${rowPrefix}_${rowId}_exercice"
          data-ajax-url="/api/get-exercices/"
          data-ajax-placeholder="Rechercher un exercice..."
          data-field="exercice"
          data-ajax-length="0">
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
        <div class="d-flex flex-row align-items-center mb-2">
          <div id="non_mandatement_visa_${rowId}" class="d-flex visa-checkboxes">
            <div class="form-check form-check-inline">
              <label class="d-flex align-items-center gap-2 dynamic-option">
                <input
                  name="${rowPrefix}_${rowId}_visa"
                  type="checkbox"
                  class="form-check-input dynamic-check"
                  data-field="statut_visa_budgetaire_oui"
                  value="True"
                  id="${rowPrefix}_${rowId}_visa-oui">
                <span>Oui</span>
              </label>
            </div>
            <div class="form-check form-check-inline">
              <label class="d-flex align-items-center gap-2 dynamic-option">
                <input
                  name="${rowPrefix}_${rowId}_visa"
                  type="checkbox"
                  class="form-check-input dynamic-check"
                  data-field="statut_visa_budgetaire_non"
                  value="False"
                  id="${rowPrefix}_${rowId}_visa-non">
                <span>Non</span>
              </label>
            </div>
          </div>
        </div>
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

  // collecte non mandatement data
  function collectNonMandatementData() {
    const data = [];

    $('#nonmandatement-collecte-tbody .dynamic-row').each(function () {
      const $row = $(this);

      const moisNonMandates = [];
      $row.find('.month-checkbox:checked').each(function () {
        moisNonMandates.push({
          mois_numero: parseInt($(this).val()),
          statut: true
        });
      });

      // Construire l'objet ligne
      const ouiChecked = $row.find('[data-field="statut_visa_budgetaire_oui"]').is(':checked');
      const nonChecked = $row.find('[data-field="statut_visa_budgetaire_non"]').is(':checked');
      const rowData = {
        Exercice: $row.find('[data-field="exercice"]').val(),
        Loyer_Mensuel: parseFloat($row.find('.loyer-mensuel').val()) || 0,
        Ref_Attestattion: $row.find('[data-field="reference"]').val(),
        Date_signature: $row.find('[data-field="date_signature"]').val(),
        mois_non_mandates: moisNonMandates,
        Montant_total_exercice: parseFloat($row.find('.montant-total').val()) || 0,
        statut_visa_budgetaire: ouiChecked ? 'True' : nonChecked ? 'False' : null,
        Ref_contrat_avenant: $row.find('[data-field="reference_contrat"]').val()
      };

      // N'ajouter que si au moins un mois est coché
      if (moisNonMandates.length > 0) {
        data.push(rowData);
      }
    });

    return data;
  }

  // Initialiser le tableau Non-Mandatement
  window.TableManagers.nonMandatementManager = new DynamicTableManager({
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
    toggleChecker: function (rowId) {
      const listId = `non_mandatement_visa_${rowId}`;
      const $list = $(`#${listId}`);
      $list.on('change', '.dynamic-check', function () {
        toggleCheck({
          listId: listId,
          checkbox: this,
          dynamicCheckClass: 'dynamic-check',
          dynamicOptionClass: 'dynamic-option',
          dynamicInputClass: 'dynamic-x-input',
          hiddenId: null
        });
      });
    },
    fields: [],
    customCollectData: collectNonMandatementData
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
