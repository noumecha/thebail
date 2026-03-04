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

  initElementsImmeuble(containerId = '#main-elements-immeuble-container') {
    // Gérer TOUS les éléments de description avec un seul événement
    const $container = $(containerId);
    $container.find('input[type="number"]').each(function () {
      $(this).prop('disabled', true).val('');
    });
    // befor rebinding :
    $(containerId).off('change', '.dynamic-check');
    // on init by default, we nee to get all element with id="element_{{ el.id }}_non" and set it checked
    $container.find('.dynamic-check').each(function () {
      const $row = $(this).closest('tr');
      const elementId = $row.data('el-id');
      $row.find(`#element_${elementId}_non`).prop('checked', true);
      $row.find(`#element_${elementId}_oui`).prop('checked', false);
    });

    $(containerId).on('change', '.dynamic-check', function () {
      const $checkbox = $(this);
      const $row = $checkbox.closest('tr');
      const elementId = $row.data('el-id');
      const context = $row.data('context');
      const listId = `immeuble_element_${elementId}_${context}`;
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
  handleServerErrors(result, form) {
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

    this.showErrors(errors.length > 0 ? errors : ['Erreur de validation inconnue'], form);
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
    if (form) {
      const oldAlerts = form.querySelectorAll('.alert-danger');
      oldAlerts.forEach(alert => alert.remove());
    }

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
    // append error on alert-block
    const errorBlock = form.querySelector('#alert-block');
    errorBlock.innerHTML = alertHtml;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  hideLoader(form = null) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = this.isEditMode
        ? '<i class="bx bx-edit"></i> Mettre à jour la fiche'
        : '<i class="bx bx-save"></i> Enregistrer la fiche';
      submitBtn.classList.add(this.isEditMode ? 'btn-warning' : 'btn-primary');
    }
  },

  showSuccess(message, form = null) {
    // Supprimer les anciennes alertes
    const oldAlerts = form.querySelectorAll('.alert-danger');
    oldAlerts.forEach(alert => alert.remove());

    // Créer une alerte de succès
    const alertHtml = `
      <div class="alert alert-success alert-dismissible fade show" role="alert">
        <h5 class="alert-heading"><i class="bx bx-check-circle"></i> Succès</h5>
        <p>${message}</p>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;
    // append error on alert-block
    const alertBlock = form.querySelector('#alert-block');
    alertBlock.innerHTML = alertHtml;
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Rediriger après 3 secondes
    setTimeout(() => {
      window.location.href = `/collecte/list/`;
    }, 3000);
  },

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
  },

  getValue(fieldId) {
    const field = document.getElementById(fieldId);
    return field ? field.value : null;
  },

  // getting checkbox value for yes or no
  getCheckboxValueYesNo(fieldId) {
    const container = $('#' + fieldId);
    const ouiChecked = container.find('[data-field=' + fieldId + '-oui]').is(':checked');
    const nonChecked = container.find('[data-field=' + fieldId + '-non]').is(':checked');
    if (ouiChecked) {
      return true;
    } else if (nonChecked) {
      return false;
    }
    return null;
  },

  // ✅ Fonction utilitaire pour convertir un fichier en base64
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result);
      };
      reader.onerror = error => {
        reject(error);
      };
      reader.readAsDataURL(file);
    });
  },

  /**
   * message an ux tips
   */
  showLoader(form = null) {
    // Afficher un message de chargement ou une animation
    if (!form) {
      showNotification('Chargement des informations...', 'info');
    }
    // Afficher un spinner ou désactiver le bouton de soumission pour indiquer que le formulaire est en cours de traitement
    if (form) {
      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Enregistrement...';
    }
  },

  /**
   * init select2 with ajax for a select element
   * @returns void
   */
  initSelect2Ajax($container = $(document), rowPrefix = null) {
    $container.find('.select2-ajax').each(function () {
      const $select = $(this);
      // Éviter de réinitialiser si déjà initialisé
      if ($select.hasClass('select2-hidden-accessible')) {
        return;
      }

      const ajaxUrl = $select.data('ajax-url');
      const placeholder = $select.data('ajax-placeholder');
      const minLengthAttr = $select.attr('data-ajax-length');
      const minLength = minLengthAttr !== undefined && minLengthAttr !== '' ? parseInt(minLengthAttr) : 2;
      // 👇 Détection automatique du bon parent
      const $modalParent = $select.closest('.modal');
      const $dropdownParent = $modalParent.length ? $modalParent : $container;

      try {
        $select.select2({
          ajax: {
            url: ajaxUrl,
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return { q: params.term || '', page: params.page || 1 };
            },
            processResults: function (data) {
              return {
                results: data.results,
                pagination: { more: data.pagination.more }
              };
            },
            error: () => {
              console.error('Erreur lors du chargement des options');
              return { results: [] };
            },
            cache: true
          },
          placeholder: placeholder || 'Rechercher...',
          minimumInputLength: minLength,
          dropdownParent: $dropdownParent,
          language: {
            inputTooShort: () => 'Veuillez saisir au moins 2 caractères',
            searching: () => 'Recherche en cours...',
            noResults: () => 'Aucun résultat trouvé'
          }
        });

        // ✅ Si minLength = 0, charger les résultats à l'ouverture (UNE SEULE FOIS)
        if (minLength === 0) {
          $select.on('select2:open', function () {
            // Charger les résultats seulement si le champ est vide
            if (!$(this).val()) {
              $(this).data('select2').trigger('query', { term: '' });
            }
          });
        }
      } catch (error) {
        console.error('Erreur Select2:', error);
      }
    });
  },

  /**
   * toggle checkbox with dynamic behavior (show/hide input, update hidden field, double unchecked)
   * @param {string} listId - the id of the checkbox list container
   * @param {HTMLElement} checkbox - the checkbox that triggered the event
   * @param {string} dynamicCheckClass - the class of the checkboxes in the list
   * @param {string} dynamicOptionClass - the class of the option container (used to find the input to show/hide)
   * @param {string} dynamicInputClass - the class of the input to show/hide
   * @param {boolean} doubleUnchecked - if true, when an option is unchecked, the other option will be checked (used for yes/no options)
   * @param {string|null} hiddenId - the id of the hidden input to update with the selected value (optional)
   * @param {function|null} onToggle - a callback function that will be called when an option is toggled, with the signature (isChecked, value) (optional)
   * @returns void
   */
  toggleCheck({
    listId,
    checkbox,
    dynamicCheckClass,
    dynamicOptionClass,
    dynamicInputClass,
    doubleUnchecked = false,
    hiddenId,
    onToggle = null
  }) {
    const $list = $('#' + listId);
    const $cb = $(checkbox);
    const label = $cb.val();

    const $container = $cb.closest('.' + dynamicOptionClass);
    const $xInput = $container.find('.' + dynamicInputClass);

    // 1️⃣ décocher les autres
    $list
      .find('.' + dynamicCheckClass)
      .not($cb)
      .prop('checked', false)
      .closest('.' + dynamicOptionClass)
      .find('.' + dynamicInputClass)
      .addClass('d-none');

    // 2️⃣ lorsque l'option cochée est décoché on coche l'autre option (oui/non) et si l'option doubleUnchecked est défini
    if (!$cb.is(':checked') && doubleUnchecked) {
      // Récupérer l'autre checkbox qui vient d'être cochée
      const $otherCb = $list.find('.' + dynamicCheckClass).not($cb);
      $otherCb
        .prop('checked', true)
        .closest('.' + dynamicOptionClass)
        .find('.' + dynamicInputClass)
        .removeClass('d-none');

      // ✅ Appeler onToggle avec les valeurs de l'AUTRE checkbox (celle qui vient d'être activée)
      onToggle && onToggle(true, $otherCb.val());
    } else {
      $xInput.removeClass('d-none').focus();
      onToggle && onToggle($cb.is(':checked'), label);
    }

    if (hiddenId) {
      const value = $cb.is(':checked') ? label : '';
      this.updateHidden(value, hiddenId);
    }
  },

  /**
   *
   */
  updateHidden(value, hiddenId) {
    $('#' + hiddenId).val(value);
  },

  /**
   *
   */
  addToList(id, label, listId) {
    const $label = $(`
      <label class="d-flex align-items-center gap-2 dynamic-option">
        <input type="checkbox"
          name="${listId}_checkbox"
          value="${id || label}"
          class="form-check-input dynamic-check">
        <span class="fw-bold">${label}</span>
      </label>
    `);

    $list = $('#' + listId);
    $list.append($label);
    $label.find('.dynamic-check').change();
  },

  /**
   * init a dynamic choice list with add new option functionality
   * @param {*} listId
   * @param {*} hiddenId
   * @param {*} newInputId
   * @param {*} formWrapper
   * @param {*} addBtnId
   * @param {*} url
   */
  initDynamicChoiceList(listId, hiddenId, newInputId, formWrapper, addBtnId, url) {
    const $list = $('#' + listId);

    $list.on('change', '.dynamic-check', function () {
      toggleCheck({
        listId: listId,
        checkbox: this,
        dynamicCheckClass: 'dynamic-check',
        dynamicOptionClass: 'dynamic-option',
        dynamicInputClass: 'dynamic-x-input',
        hiddenId: hiddenId
      });
    });

    // save option to db and add to the list
    $('#' + addBtnId).click(function () {
      const val = $('#' + newInputId)
        .val()
        .trim();
      if (!val) return;
      console.log('token: ', this.getCSRFToken(formWrapper));
      console.log('list id ', listId);
      console.log('data sent: ', { label: val, model: $('#' + listId).data('model') });
      if (url) {
        $.post({
          url: url,
          data: {
            label: val,
            model: $('#' + listId).data('model')
          },
          headers: {
            'X-CSRFToken': this.getCSRFToken(formWrapper)
          }
        }).done(function (res) {
          this.addToList(res.id, res.label, listId);
        });
      } else {
        this.addToList(null, val, listId);
      }
      $('#' + newInputId).val('');
    });
  },

  /**
   * get csrf token from cookie or from form input
   */
  getCSRFToken(formWrapper = null) {
    if (formWrapper) {
      const token = $('#' + formWrapper)
        .find('input[name="csrfmiddlewaretoken"]')
        .val();
      if (token) return token;
    }
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith('csrftoken=')) {
        return cookie.substring('csrftoken='.length);
      }
    }
    return '';
  },

  /**
   * for dynamic elements
   */

  // form for element inside another form
  addElementToList(listId, newInputId, addBtnId, url) {
    const selectContainer = $(listId);
    $('#' + addBtnId).click(function () {
      const val = $('#' + newInputId)
        .val()
        .trim();
      if (!val) return;
      if (url) {
        $.post({
          url: url,
          data: {
            libelle: val,
            model: selectContainer.data('model')
          },
          headers: {
            'X-CSRFToken': FormUtils.getCSRFToken()
          }
        }).done(function (data) {
          console.log('data : ', data);
          if (data.html) {
            FormUtils.appendToDynamicGroup(listId, data.html);
          }
          if (data.success) {
            FormUtils.showAlertMessage(data.message, `${listId}-form-success`, 3000);
          } else {
            FormUtils.showAlertMessage(data.errors, `${listId}-form-error`, 3000);
          }
        });
      } else {
        FormUtils.showAlertMessage(data.message, `${listId}-form-error`, 3000);
      }
      $('#' + newInputId).val('');
    });
  },
  GROUP_HEADERS: {
    element: `
    <thead class="table-light">
      <tr>
        <th class="bg-secondary-subtle text-capitalize p-0">Existence</th>
        <th class="p-0"></th>
        <th class="bg-secondary-subtle text-capitalize p-0">Quantité</th>
      </tr>
    </thead>
  `,
    piece: `
    <thead class="table-light">
      <tr>
        <th class="p-0">Désignation</th>
        <th class="p-0">Quantité</th>
        <th class="p-0">Images</th>
      </tr>
    </thead>
  `
  },
  appendToDynamicGroup(containerSelector, newRowHtml) {
    const $container = $(containerSelector);
    console.log('container : ', $container);
    const groupType = $container.data('group-type');
    console.log('group type : ', groupType);
    const maxItems = parseInt($container.data('max-items')) || 9;

    // Find last group
    let $lastGroup = $container.find('.col-block').last();

    // If no group exists, create one
    if (!$lastGroup.length) {
      $lastGroup = FormUtils.createNewGroup($container, groupType);
      $container.append($lastGroup);
    }

    const $tbody = $lastGroup.find('tbody');
    const currentCount = $tbody.find('tr').length;

    // If last group is full, create a new one
    if (currentCount >= maxItems) {
      const $newGroup = FormUtils.createNewGroup($container, groupType);
      $container.append($newGroup);
      $newGroup.find('tbody').append(newRowHtml);
    } else {
      $tbody.append(newRowHtml);
    }
  },

  createNewGroup($container, type) {
    const headerHtml = FormUtils.GROUP_HEADERS[type] || '';
    const colClass = type === 'piece' ? 'col-md-6 col-lg-4' : 'col-md-4';

    const $newGroup = $(`
    <div class="${colClass} col-block mb-4">
      <table class="table align-middle text-center">
        ${headerHtml}
        <tbody class="${type}-collecte-container-tbody"></tbody>
      </table>
    </div>
  `);

    return $newGroup;
  },
  showAlertMessage(msg, id, timeout = 5000) {
    const msgBlock = $(id);
    msgBlock.stop(true, true).empty();

    if (typeof msg === 'object' && !Array.isArray(msg)) {
      // Handle JSON object with fields and arrays of messages
      const list = $('<ul></ul>');
      Object.keys(msg).forEach(key => {
        msg[key].forEach(error => {
          list.append($('<li></li>').text(`${key}: ${error}`));
        });
      });
      msgBlock.append(list);
    } else {
      // Handle string messages
      msgBlock.append($('<p class="text-center mb-0"></p>').text(msg));
    }

    msgBlock.fadeIn().css('display', 'block');
    setTimeout(() => msgBlock.fadeOut(), timeout);
  }
};
