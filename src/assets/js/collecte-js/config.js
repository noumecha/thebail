import { DynamicTableManager } from './modules/tables-manager.js';
window.configs = window.configs || {};
window.configs.customMessages = {
  // Erreurs par champ spécifique
  'immeuble.type_construction_id': 'Veuillez sélectionner un type de construction',
  'immeuble.Date_Construction': "Veuillez définir la date de construction de l'immeuble",
  'immeuble.type_location_id': 'Veuillez sélectionner un type de location',
  'immeuble.statut_batisse_id': 'Veuillez sélectionner un statut de bâtisse',
  'immeuble.revetement_int_id': 'Veuillez sélectionner un type de revêtement intérieur',
  'immeuble.revetement_ext_id': 'Veuillez sélectionner un type de revêtement extérieur',
  'immeuble.Designation': 'Veuillez saisir la désignation du bien',
  'contrat.bailleur.Type_personne': 'Veuillez sélectionner le type de personne du bailleur',
  'contrat.Duree_Contrat': 'Veuillez saisir la durée du contrat',
  'bailleur.Nom_prenom': 'Veuillez saisir le noms & prénoms/Raison social du bailleur'
};
window.configs.genericMessages = {
  'Un nombre entier valide est requis.': 'Veuillez sélectionner une option valide',
  'Ce champ est obligatoire.': 'Ce champ est requis',
  'This field is required.': 'Ce champ est requis',
  'A valid integer is required.': 'Veuillez sélectionner une option valide',
  'Enter a valid email address.': 'Veuillez saisir une adresse email valide'
};
// ─── Non-mandatement helpers ──────────────────────────────────────────────────

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

// ─── Initialisation ───────────────────────────────────────────────────────────
let tableManagers = {};
function initTableManagers() {
  // Événements délégués pour non-mandatement
  $('#nonmandatement-collecte-tbody').on('input change', '.loyer-mensuel', function () {
    calculateMontantTotal($(this).closest('.dynamic-row'));
  });
  $('#nonmandatement-collecte-tbody').on('change', '.month-checkbox', function () {
    calculateMontantTotal($(this).closest('.dynamic-row'));
  });
  tableManagers = {
    ayantsDroitManager: new DynamicTableManager({
      tbodyId: 'ayants-droit-tbody',
      addButtonId: 'add-ayant-droit-row',
      tableId: 'ayants-droit-table',
      rowPrefix: 'ayant_droit',
      autoAdd: true,
      minRows: 1,
      showRowNumber: true,
      fields: [
        { name: 'Nom_Prenom_ayant_droit', type: 'text', placeholder: 'Nom & Prénoms' },
        { name: 'Contact_ayant_droit', type: 'text', placeholder: 'Contact' },
        { name: 'Reference_Grosse_ayant_droit', type: 'text', placeholder: 'Référence Grosse' },
        { name: 'Date_delivrance_grosse', type: 'date' },
        { name: 'Reference_certificat_non_appel', type: 'text', placeholder: 'Référence Certificat' },
        { name: 'Date_delivrance_certificat_non_appel', type: 'date' }
      ]
    }),

    logementsManager: new DynamicTableManager({
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
    }),

    bureauxManager: new DynamicTableManager({
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
    }),

    nonMandatementManager: new DynamicTableManager({
      tbodyId: 'nonmandatement-collecte-tbody',
      addButtonId: 'add-nonmandatement-row',
      tableId: 'nonmandatement-collecte-table',
      rowPrefix: 'nonmandatement',
      autoAdd: false,
      minRows: 1,
      customTemplate: getNonMandatementTemplate,
      onRowCreated: $row => {
        $row.find('.loyer-mensuel').on('input change', () => calculateMontantTotal($row));
        $row.find('.month-checkbox').on('change', () => calculateMontantTotal($row));
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
    })
  };
}
$(function () {
  initTableManagers();
});
export { tableManagers, initTableManagers };
