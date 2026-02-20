/**
 * modules des fonctions utiles du formulaires
 */

export const FormUtils = {
  initPiecesCollectees() {
    const $container = $('.pieces-collecte-container-tbody');

    $container.find('input[type="number"]').each(function () {
      $(this).prop('disabled', true).val('');
    });
    $container.find('input[type="file"]').each(function () {
      $(this).prop('disabled', true).val('');
    });

    // ✅ Gestion du checkbox
    $container.on('change', '.piece-checkbox', function () {
      const $checkbox = $(this);
      const $row = $checkbox.closest('tr');
      const elementId = $row.data('piece-id');
      const $numberInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $fileInput = $row.find(`#piece_image_input_${elementId}`);
      const $fileLabel = $row.find(`label[for="piece_image_input_${elementId}"]`);

      if ($checkbox.is(':checked')) {
        $numberInput.prop('disabled', false).val('1');
        $fileInput.prop('disabled', false);
        // Initialiser avec max = 1
        updateFileInputLimit($fileInput, 1, $fileLabel);
        $numberInput.focus();
      } else {
        $numberInput.prop('disabled', true).val('');
        $fileInput.prop('disabled', true).val('');
        $fileLabel.text('0 fich.');
        updateFileInputLimit($fileInput, 1, $fileLabel);
      }
    });

    // ✅ Gestion du changement de quantité
    $container.on('change input', '.piece-nombre', function () {
      const $numberInput = $(this);
      const $row = $numberInput.closest('tr');
      const elementId = $row.data('piece-id');
      const $fileInput = $row.find(`#piece_image_input_${elementId}`);
      const $fileLabel = $row.find(`label[for="piece_image_input_${elementId}"]`);
      const quantity = parseInt($numberInput.val()) || 1;

      // Réinitialiser le file input si la quantité change
      $fileInput.val('');
      $fileLabel.text('0 fich.');
      updateFileInputLimit($fileInput, quantity, $fileLabel);
    });

    // ✅ Gestion de la sélection des fichiers
    $container.on('change', '.piece-files', function () {
      const $fileInput = $(this);
      const $row = $fileInput.closest('tr');
      const elementId = $row.data('piece-id');
      const $numberInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $fileLabel = $row.find(`label[for="piece_image_input_${elementId}"]`);
      const maxFiles = parseInt($numberInput.val()) || 1;
      const selectedFiles = this.files;

      // ✅ Vérifier si l'utilisateur a sélectionné trop de fichiers
      if (selectedFiles.length > maxFiles) {
        showFileError($fileInput, $fileLabel, maxFiles, selectedFiles.length);
        // Réinitialiser le file input
        $fileInput.val('');
        $fileLabel.text('0 fich.');
        return;
      }

      // ✅ Mettre à jour le label
      $fileLabel.text(`${selectedFiles.length} fich.`);
      clearFileError($fileInput);
    });
  },

  initElementsImmeuble() {
    // Gérer TOUS les éléments de description avec un seul événement
    const $container = $('#elements-immeuble-container');
    $container.find('input[type="number"]').each(function () {
      $(this).prop('disabled', true).val('');
    });
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
        doubleUnchecked: true,
        hiddenId: null,
        // function to surcharge toggleCheck (setting number to 1 when oui is checked and setting number to empty when non is checked)
        onToggle: (isChecked, checkboxValue) => {
          const $row = $(this).closest('tr');
          const elementId = $row.data('el-id');
          const $numberInput = $row.find(`#nombre_input_${elementId}`);
          if (isChecked && checkboxValue === 'oui') {
            $numberInput.prop('disabled', false).focus();
            $numberInput.val('1');
          } else {
            $numberInput.prop('disabled', true).val('');
          }
        }
      });
    });
  },

  // ✅ Gérer les erreurs du serveur de manière structurée
  handleServerErrors(result) {
    const errors = [];

    if (result.message) {
      errors.push(result.message);
    }

    if (result.errors) {
      // Aplatir les erreurs imbriquées
      const flatErrors = flattenErrors(result.errors);

      flatErrors.forEach(({ field, message }) => {
        const label = this.getFieldLabel(field);
        const customMessage = this.getCustomErrorMessage(field, message);
        errors.push(`${label}: ${customMessage}`);
      });
    }

    this.showErrors(errors.length > 0 ? errors : ['Erreur de validation inconnue']);
  },

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
  },

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
  },

  showErrors(errors, form = null) {
    // Supprimer les anciennes alertes
    const oldAlerts = form.querySelectorAll('.alert-danger');
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

    form.insertAdjacentHTML('afterbegin', alertHtml);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  hideLoader(form = null) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = this.isEditMode
        ? '<i class="bx bx-edit"></i> Mettre à jour'
        : '<i class="bx bx-save"></i> Enregistrer';
      submitBtn.classList.add(this.isEditMode ? 'btn-warning' : 'btn-primary');
    }
  },

  showSuccess(message, ficheId, form = null) {
    // Supprimer les anciennes alertes
    const oldAlerts = form.querySelectorAll('.alert-danger');
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

    form.insertAdjacentHTML('afterbegin', alertHtml);
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Rediriger après 3 secondes
    setTimeout(() => {
      window.location.href = `/collecte/list/`;
    }, 3000);
  }
};
