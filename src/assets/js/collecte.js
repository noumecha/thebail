// collecte.js
class FicheCollecteFormHandler {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.init();
  }

  init() {
    this.form.addEventListener('submit', e => {
      e.preventDefault();
      this.handleSubmit();
    });
    // generate numero collecte
    $('#arrondissement').on('select2:select', e => {
      const arrondissementId = e.params.data.id;
      if (arrondissementId) {
        this.generateFicheCollecte(arrondissementId);
      }
    });
    // init pieces an elements states
    this.initElementsImmeuble();
    this.initPiecesCollectees();
  }

  initPiecesCollectees() {
    const $container = $('.pieces-collecte-container-tbody');
    $container.find('input[type="number"]').each(function () {
      $(this).prop('disabled', true).val('');
    });
    $container.find('input[type="file"]').each(function () {
      $(this).prop('disabled', true).val('');
    });
    $container.on('change', '.piece-checkbox', function () {
      const $checkbox = $(this);
      const $row = $checkbox.closest('tr');
      const elementId = $row.data('piece-id');
      const $numberInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $fileInput = $row.find(`#piece_image_input_${elementId}`);

      if ($checkbox.is(':checked')) {
        $numberInput.prop('disabled', false).focus();
        $fileInput.prop('disabled', false).focus();
      } else {
        $numberInput.prop('disabled', true).val('');
        $fileInput.prop('disabled', true).val('');
      }
    });
  }

  validatePiecesCollectees() {
    const errors = [];
    const $container = $('#pieces-collecte-container-tbody');
    $container.find('tr[data-piece-id]').each(function () {
      const $row = $(this);
      const elementId = $row.data('piece-id');
      const $checkbox = $row.find(`#piece_${elementId}`);
      const $numberInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $imageInput = $row.find(`#piece_image_input_${elementId}`);
      const elementLabel = $row.find('label.form-check-label').text().trim();
      if ($checkbox.is(':checked')) {
        const quantity = $numberInput.val();
        const images = $imageInput.val();
        if (!quantity || quantity.trim() === '' || parseInt(quantity) <= 0) {
          errors.push(`${elementLabel}: La quantité est obligatoire lorsque l'élément est coché`);
        }
        if (!images || images.length <= 0) {
          errors.push(`${elementLabel}: Les images sont obligatoires lorsque l'élément est coché`);
        }
      }
    });
    return errors;
  }

  initElementsImmeuble() {
    const $container = $('#elements-immeuble-container');
    $container.find('input[type="number"]').each(function () {
      $(this).prop('disabled', true).val('');
    });

    $container.on('change', '.dynamic-check', function () {
      const $checkbox = $(this);
      const $row = $checkbox.closest('tr');
      const elementId = $row.data('el-id');
      const $numberInput = $row.find(`#nombre_input_${elementId}`);
      const checkboxValue = $checkbox.val();

      if ($checkbox.is(':checked') && checkboxValue === 'oui') {
        $numberInput.prop('disabled', false).focus();
      } else {
        $numberInput.prop('disabled', true).val('');
      }
    });
  }

  validateElementsImmeuble() {
    const errors = [];
    const $container = $('#elements-immeuble-container');

    $container.find('tr[data-el-id]').each(function () {
      const $row = $(this);
      const elementId = $row.data('el-id');
      const $ouiCheckbox = $row.find(`#element_${elementId}_oui`);
      const $numberInput = $row.find(`#nombre_input_${elementId}`);
      const elementLabel = $row.find('label.text-capitalize').text().trim();

      if ($ouiCheckbox.is(':checked')) {
        const quantity = $numberInput.val();
        if (!quantity || quantity.trim() === '' || parseInt(quantity) <= 0) {
          errors.push(`${elementLabel}: La quantité est obligatoire lorsque "Oui" est sélectionné`);
        }
      }
    });

    return errors;
  }

  // Collecter toutes les données du formulaire
  collectFormData() {
    // Vérifier que les managers sont disponibles
    if (!window.TableManagers) {
      console.error('TableManagers not initialized');
      throw new Error('Les gestionnaires de tableaux ne sont pas initialisés');
    }
    const data = {
      Numero_fiche_de_collecte: this.getValue('Numero_fiche_de_collecte'),
      agent_collecte_id: this.getValue('responsable_collecte'),
      matricule_agent: this.getValue('matricule_responsable_collecte'),
      Date_de_collecte: this.getValue('Date_de_collecte'),
      immeuble: {
        Designation: this.getValue('Designation'),
        type_construction_id: this.getDynamicChoiceValue('type_construction_id'),
        type_location_id: this.getDynamicChoiceValue('type_location_id'),
        Date_Construction: this.getValue('Date_Construction'),
        Nombre_de_pieces: this.getValue('Nombre_de_pieces'),
        Superficie_louer: this.getValue('Superficie_louer'),
        statut_batisse_id: this.getDynamicChoiceValue('statut_batisse_id'),
        revetement_int_id: this.getDynamicChoiceValue('revetement_int_id'),
        revetement_ext_id: this.getDynamicChoiceValue('revetement_ext_id'),
        observation: this.getValue('observation'),
        localisation: {
          pays: this.getValue('pays'),
          Ville: this.getValue('Ville'),
          Rue: this.getValue('Rue'),
          region: this.getValue('region'),
          departement: this.getValue('departement'),
          arrondissement: this.getValue('arrondissement'),
          Quartier: this.getValue('Quartier'),
          Coordonee_gps: this.getValue('Coordonee_gps')
        },
        elements_description: this.collectElementsDescription(),
        occupants_residents: window.TableManagers.logementsManager?.collectData() || [],
        occupants_bureaux: window.TableManagers.bureauxManager?.collectData() || []
      },
      contrat: {
        TypeContrat: this.getDynamicChoiceValue('TypeContrat'),
        Numero_contrat: this.getValue('Numero_contrat'),
        Date_Signature_contrat: this.getValue('Date_Signature_contrat'),
        Fonction_signataire_contrat: this.getValue('Fonction_signataire_contrat'),
        Date_effet_contrat: this.getValue('Date_effet_contrat'),
        Existence_visa_budgétaire: this.getCheckboxValue('Existence_visa_budgétaire'),
        Duree_Contrat: this.getValue('Duree_Contrat'),
        Tacite_reconduction_contrat: this.getCheckboxValue('Tacite_reconduction_contrat'),
        Regime_fiscal_contrat: this.getValue('Regime_fiscal_contrat'),
        Montant_loyer_mensuel: this.getValue('Montant_loyer_mensuel'),
        Devise: this.getValue('Devise'),
        Periodicite_Reglement_id: this.getDynamicChoiceValue('Periodicite_Reglement_id'),
        Existence_avenant: this.getCheckboxValue('Existence_avenant'),
        bailleur: {
          Type_personne: this.getDynamicChoiceValue('Type_personne'),
          Raison_social: this.getValue('Raison_social'),
          Nom_Prenom_Representant: this.getValue('Nom_Prenom_Representant'),
          Domicille_siege_social_bailleur: this.getValue('Domicille_siege_social_bailleur'),
          NIU: this.getValue('NIU'),
          Telephone: this.getValue('Telephone'),
          Num_doc: this.getValue('Num_doc'),
          Date_delivrance_doc: this.getValue('Date_delivrance_doc'),
          Statut_bailleur: this.getDynamicChoiceValue('Statut_bailleur'),
          Banque: this.getValue('Banque'),
          RIB: this.getValue('RIB'),
          Intitule_compte: this.getValue('Intitule_compte'),
          ayants_droit: window.TableManagers.ayantsDroitManager?.collectData() || []
        },
        avenants: this.collectAvenants(),
        non_mandatements: window.TableManagers.nonMandatementManager?.collectData() || []
      },
      pieces_collectees: this.collectPiecesCollectees()
    };
    return data;
  }

  // getting values method
  getValue(fieldId) {
    const field = document.getElementById(fieldId);
    return field ? field.value : null;
  }

  getDynamicChoiceValue(listId, returnId = true) {
    const $list = document.getElementById(listId);
    if (!$list) return null;

    const checkedCheckbox = $list.querySelector('.dynamic-check:checked');
    if (!checkedCheckbox) return null;

    if (returnId) {
      // ✅ Retourner l'ID pour Django
      return checkedCheckbox.getAttribute('data-choice-id') || checkedCheckbox.value;
    } else {
      // Retourner le libellé
      const label = checkedCheckbox.closest('.dynamic-option');
      return label ? label.querySelector('span').textContent.trim() : null;
    }
  }

  getCheckboxValue(fieldId) {
    const checkbox = document.getElementById(fieldId);
    return checkbox ? checkbox.checked : false;
  }

  // Collecter les éléments de description
  collectElementsDescription() {
    const elements = [];
    document.querySelectorAll('.elements-immeuble-container-tbody tr').forEach(row => {
      const elementId = row.dataset.elId;
      const ouiChecked = row.querySelector(`#element_${elementId}_oui`)?.checked;
      const nonChecked = row.querySelector(`#element_${elementId}_non`)?.checked;
      const nombre = row.querySelector(`input[type="number"]`)?.value || 0;

      if (ouiChecked || nonChecked) {
        elements.push({
          element_id: parseInt(elementId),
          statut: ouiChecked ? true : nonChecked ? false : null,
          nombre: parseInt(nombre)
        });
      }
    });
    return elements;
  }

  // Collecter les avenants
  collectAvenants() {
    const avenants = [];

    // Avenant 1
    const avenant1 = {
      Ref_Avenant: this.getValue('reference_avenant_1'),
      Date_Signature: this.getValue('date_signature_avenant_1'),
      Date_effet: this.getValue('date_effet_avenant_1'),
      Ancien_bailleur: this.getValue('avenant_1_ancien_bailleurs_list'),
      Nouveau_bailleur: this.getValue('avenant_1_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: this.getValue('avenant_1_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: this.getValue('avenant_1_nouveaumontant_loyer_mensuel')
    };

    if (avenant1.Ref_Avenant) {
      avenants.push(avenant1);
    }

    // Avenant 2
    const avenant2 = {
      Ref_Avenant: this.getValue('reference_avenant_2'),
      Date_Signature: this.getValue('date_signature_avenant_2'),
      Date_effet: this.getValue('date_effet_avenant_2'),
      Ancien_bailleur: this.getValue('avenant_2_ancien_bailleurs_list'),
      Nouveau_bailleur: this.getValue('avenant_2_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: this.getValue('avenant_2_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: this.getValue('avenant_2_nouveaumontant_loyer_mensuel')
    };

    if (avenant2.Ref_Avenant) {
      avenants.push(avenant2);
    }

    return avenants;
  }

  // Collecter les pièces collectées
  collectPiecesCollectees() {
    const pieces = [];
    document.querySelectorAll('.piece-row').forEach(row => {
      const pieceId = row.dataset.pieceId;
      const checkbox = row.querySelector('.piece-checkbox');
      const nombreInput = row.querySelector('.piece-nombre');
      const files = row.querySelector('.piece-files');

      if (checkbox?.checked) {
        pieces.push({
          piece_id: parseInt(pieceId),
          statut: true,
          nombre: parseInt(nombreInput?.value || 1),
          images: Array.from(files.files).map(file => URL.createObjectURL(file))
        });
      }
    });
    return pieces;
  }

  // Valider les données avant soumission
  validateData(data) {
    const errors = [];

    // Validations de base
    if (!data.Numero_fiche_de_collecte) {
      errors.push('Le numéro de fiche de collecte est requis');
    }

    if (!data.Date_de_collecte) {
      errors.push('La date de collecte est requise');
    }

    if (!data.agent_collecte_id) {
      errors.push('Le responsable de collecte est requis');
    }

    if (!data.immeuble.Designation) {
      errors.push('La désignation du bien est requise');
    }

    if (!data.immeuble.type_construction_id) {
      errors.push('Le type de construction est requis');
    }

    if (!data.contrat.Numero_contrat) {
      errors.push('Le numéro de contrat est requis');
    }

    if (!data.contrat.bailleur.Raison_social) {
      errors.push('Le nom du bailleur est requis');
    }

    // valider les pièces collectées
    const pieceErrors = this.validatePiecesCollectees();
    if (pieceErrors.length > 0) {
      errors.push(...pieceErrors);
    }
    // Valider les éléments d'immeuble
    const elementErrors = this.validateElementsImmeuble();
    if (elementErrors.length > 0) {
      errors.push(...elementErrors);
    }

    return errors;
  }

  // Soumettre le formulaire
  async handleSubmit() {
    try {
      // Afficher un loader
      this.showLoader();

      // Collecter les données
      const formData = this.collectFormData();

      // ✅ DEBUG : Afficher les données avant envoi
      console.log('📤 Données envoyées:', JSON.stringify(formData, null, 2));

      // Valider les données
      const errors = this.validateData(formData);
      if (errors.length > 0) {
        this.showErrors(errors);
        this.hideLoader();
        return;
      }

      // Envoyer les données à l'API
      const response = await fetch('/api/fiches/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken()
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      // ✅ DEBUG : Afficher la réponse
      console.log('📥 Réponse serveur:', result);

      if (response.ok && result.success) {
        this.showSuccess(result.message, result.data?.numero_fiche);
      } else {
        this.showErrors([result.message || 'Erreur lors de la soumission']);
        this.handleServerErrors(result);
        console.error('Erreurs de validation:', result.errors);
      }
    } catch (error) {
      console.error('Erreur:', error);
      this.showErrors(['Une erreur est survenue lors de la soumission']);
    } finally {
      this.hideLoader();
    }
  }

  // ✅ Fonction récursive pour aplatir les erreurs imbriquées
  flattenErrors(errors, prefix = '') {
    const flatErrors = [];

    Object.entries(errors).forEach(([field, value]) => {
      const fullField = prefix ? `${prefix}.${field}` : field;

      if (Array.isArray(value)) {
        // C'est un tableau d'erreurs
        value.forEach(err => {
          flatErrors.push({
            field: fullField,
            message: err
          });
        });
      } else if (typeof value === 'object' && value !== null) {
        // C'est un objet imbriqué, récursion
        flatErrors.push(...this.flattenErrors(value, fullField));
      } else {
        // C'est une erreur simple
        flatErrors.push({
          field: fullField,
          message: value
        });
      }
    });

    return flatErrors;
  }

  // ✅ Gérer les erreurs du serveur de manière structurée
  handleServerErrors(result) {
    const errors = [];

    if (result.message) {
      errors.push(result.message);
    }

    if (result.errors) {
      // Aplatir les erreurs imbriquées
      const flatErrors = this.flattenErrors(result.errors);

      flatErrors.forEach(({ field, message }) => {
        const label = this.getFieldLabel(field);
        const customMessage = this.getCustomErrorMessage(field, message);
        errors.push(`${label}: ${customMessage}`);
      });
    }

    this.showErrors(errors.length > 0 ? errors : ['Erreur de validation inconnue']);
  }

  // ✅ Messages d'erreur personnalisés
  getCustomErrorMessage(field, originalMessage) {
    // Mapping des erreurs génériques vers des messages personnalisés
    const customMessages = window.configs.customMessages;
    // Si un message personnalisé existe pour ce champ
    if (customMessages[field]) {
      return customMessages[field];
    }
    // Sinon, traduire les messages génériques
    const genericMessages = window.configs.genericMessages;

    return genericMessages[originalMessage] || originalMessage;
  }

  // ✅ Traduire les noms de champs en labels lisibles
  getFieldLabel(field) {
    const labels = {
      // Champs de la fiche
      date_collecte: 'Date de collecte',
      agent_collecte_id: 'Responsable de collecte',
      matricule_agent: 'Matricule',

      // Champs de l'immeuble
      'immeuble.Designation': 'Désignation du bien',
      'immeuble.designation_bien': 'Désignation du bien',
      'immeuble.type_construction_id': 'Type de construction',
      'immeuble.type_location_id': 'Type de location',
      'immeuble.date_construction': 'Date de construction',
      'immeuble.nombre_pieces': 'Nombre de pièces',
      'immeuble.superficie_louee': 'Superficie louée',
      'immeuble.statut_batisse_id': 'Statut de la bâtisse',
      'immeuble.revetement_int_id': 'Revêtement intérieur',
      'immeuble.revetement_ext_id': 'Revêtement extérieur',

      // Localisation
      'immeuble.localisation.pays_id': 'Pays',
      'immeuble.localisation.ville': 'Ville',
      'immeuble.localisation.region_id': 'Région',

      // Contrat
      'contrat.numero_contrat': 'Numéro de contrat',
      'contrat.type_contrat_id': 'Type de contrat',
      'contrat.date_signature': 'Date de signature',
      'contrat.montant_loyer_mensuel': 'Montant du loyer',
      'contrat.Duree_Contrat': 'Durée du contrat',

      // Bailleur
      'contrat.bailleur.Type_personne': 'Type de personne',
      'contrat.bailleur.nom_prenom_raison_sociale': 'Nom du bailleur',
      'contrat.bailleur.niu': 'NIU',
      'contrat.bailleur.telephone': 'Téléphone'
    };

    return labels[field] || field.split('.').pop();
  }

  // ✅ Générer le numéro de fiche de collecte
  async generateFicheCollecte(arrondissementId) {
    try {
      const response = await fetch(`/api/fiches/numero/?arrondissement_id=${arrondissementId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken()
        }
      });
      const result = await response.json();
      if (response.ok && result.success) {
        const numeroField = document.getElementById('Numero_fiche_de_collecte');
        if (numeroField) {
          numeroField.value = result.numero_collecte;
          this.showNotification('Numéro de fiche généré automatiquement', 'success');
        }
        // also set automatically region an departement values
        const region_select = $('#region');
        const departement_select = $('#departement');

        let regionId = result.region_id;
        let departementId = result.dpt_id;
        let region_libelle = result.region;
        let departement_libelle = result.departement;

        region_select.val(regionId).trigger('change');
        departement_select.val(departementId).trigger('change');

        let $region_option = region_select.find('option[value="' + regionId + '"]');
        let $departement_option = departement_select.find('option[value="' + departementId + '"]');

        if ($region_option.length) {
          $region_option.text(region_libelle);
        } else {
          region_select.append(new Option(region_libelle, regionId, true, true));
          region_select.trigger('change');
        }

        if ($departement_option.length) {
          $departement_option.text(departement_libelle);
        } else {
          departement_select.append(new Option(departement_libelle, departementId, true, true));
          departement_select.trigger('change');
        }
      } else {
        console.error('Erreur génération numéro:', result.error);
        this.showNotification(result.error || 'Erreur lors de la génération du numéro', 'warning');
      }
    } catch (error) {
      console.error('❌ Erreur génération numéro:', error);
      this.showNotification('Erreur lors de la génération du numéro de fiche', 'danger');
    }
  }

  // Utilitaires
  getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  }

  // message an ux tips
  showLoader() {
    // Afficher un spinner ou désactiver le bouton
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Enregistrement...';
    }
  }

  showErrors(errors) {
    // Supprimer les anciennes alertes
    const oldAlerts = this.form.querySelectorAll('.alert-danger');
    oldAlerts.forEach(alert => alert.remove());

    const alertHtml = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <h5 class="alert-heading">
          <i class="bx bx-error-circle"></i> Erreurs de validation
        </h5>
        <ul class="mb-0">
          ${errors.map(error => `<li>${error}</li>`).join('')}
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;

    this.form.insertAdjacentHTML('afterbegin', alertHtml);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  hideLoader() {
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Enregistrer';
    }
  }

  showSuccess(message, ficheId) {
    // Supprimer les anciennes alertes
    const oldAlerts = this.form.querySelectorAll('.alert-danger');
    oldAlerts.forEach(alert => alert.remove());

    // Créer une alerte de succès
    const alertHtml = `
      <div class="alert alert-success alert-dismissible fade show" role="alert">
        <h5 class="alert-heading"><i class="bx bx-check-circle"></i> Succès</h5>
        <p>${message}</p>
        <p class="mb-0">Numéro de fiche: <strong>${ficheId}</strong></p>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;

    this.form.insertAdjacentHTML('afterbegin', alertHtml);
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Rediriger après 3 secondes
    setTimeout(() => {
      window.location.href = `/collecte/list/`;
    }, 3000);
  }

  // ✅ Notification discrète (toast)
  showNotification(message, type = 'info') {
    const toastHtml = `
      <div class="toast align-items-center text-white bg-${type} border-0 position-fixed top-0 end-0 m-3"
        role="alert"
        style="z-index: 9999;">
        <div class="d-flex">
          <div class="toast-body">
            ${message}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.querySelector('.toast:last-child');
    const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();

    // Supprimer après affichage
    toastElement.addEventListener('hidden.bs.toast', () => {
      toastElement.remove();
    });
  }
}

$(function () {
  // there the form validation and submission
  const formHandler = new FicheCollecteFormHandler('ficheCollecteForm');
});
