// collecte.js
class FicheCollecteFormHandler {
  constructor(formId, ficheId = null) {
    this.form = document.getElementById(formId);
    this.ficheId = ficheId;
    this.isEditMode = ficheId !== '';
    this.init();
  }

  async init() {
    this.form.addEventListener('submit', e => {
      e.preventDefault();
      this.handleSubmit();
    });
    // init pieces and elements states
    this.initElementsImmeuble();
    this.initPiecesCollectees();
    // mode :
    if (this.isEditMode) {
      await this.loadFicheData();
    }
    // generate numero collecte
    $('#arrondissement').on('select2:select', e => {
      const arrondissementId = e.params.data.id;
      if (arrondissementId) {
        this.generateFicheCollecte(arrondissementId);
      }
    });
    // change btn text value base on the mode :
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.innerHTML = this.isEditMode
        ? '<i class="bx bx-edit"></i> Mettre à jour la fiche'
        : '<i class="bx bx-save"></i> Enregistrer la fiche';
      submitBtn.classList.add(this.isEditMode ? 'btn-warning' : 'btn-primary');
    }
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
        // ✅ Valider la quantité
        const quantity = $numberInput.val();
        if (!quantity || quantity.trim() === '' || parseInt(quantity) <= 0) {
          errors.push(`${elementLabel}: La quantité est obligatoire lorsque l'élément est coché`);
        }

        // ✅ Valider les images (nouvelles OU existantes)
        const hasNewImages = $imageInput && $imageInput.files && $imageInput.files.length > 0;
        const hasExistingImages = $row.find('.existing-image-item').length > 0;

        if (!hasNewImages && !hasExistingImages) {
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
  async collectFormData() {
    // Vérifier que les managers sont disponibles
    if (!window.TableManagers) {
      console.error('TableManagers not initialized');
      throw new Error('Les gestionnaires de tableaux ne sont pas initialisés');
    }
    const data = {
      Numero_fiche_de_collecte: getValue('Numero_fiche_de_collecte'),
      agent_collecte_id: getValue('responsable_collecte'),
      matricule_agent: getValue('matricule_responsable_collecte'),
      Date_de_collecte: getValue('Date_de_collecte'),
      immeuble: {
        Designation: getValue('Designation'),
        type_construction_id: this.getDynamicChoiceValue('type_construction_id'),
        type_location_id: this.getDynamicChoiceValue('type_location_id'),
        Date_Construction: getValue('Date_Construction'),
        Nombre_de_pieces: getValue('Nombre_de_pieces'),
        Superficie_louer: getValue('Superficie_louer'),
        statut_batisse_id: this.getDynamicChoiceValue('statut_batisse_id'),
        revetement_int_id: this.getDynamicChoiceValue('revetement_int_id'),
        revetement_ext_id: this.getDynamicChoiceValue('revetement_ext_id'),
        observation: getValue('observation'),
        pays: getValue('pays'),
        Ville: getValue('Ville'),
        Rue: getValue('Rue'),
        region: getValue('region'),
        departement: getValue('departement'),
        arrondissement: getValue('arrondissement'),
        Quartier: getValue('Quartier'),
        Coordonee_gps: getValue('Coordonee_gps'),
        elements_description: this.collectElementsDescription(),
        occupants_residents: window.TableManagers.logementsManager?.collectData() || [],
        occupants_bureaux: window.TableManagers.bureauxManager?.collectData() || []
      },
      contrat: {
        TypeContrat: this.getDynamicChoiceValue('TypeContrat'),
        Numero_contrat: getValue('Numero_contrat'),
        Date_Signature_contrat: getValue('Date_Signature_contrat'),
        Fonction_signataire_contrat: getValue('Fonction_signataire_contrat'),
        Date_effet_contrat: getValue('Date_effet_contrat'),
        Existence_visa_budgétaire: getCheckboxValue('Existence_visa_budgétaire'),
        Duree_Contrat: getValue('Duree_Contrat'),
        Tacite_reconduction_contrat: getCheckboxValue('Tacite_reconduction_contrat'),
        Regime_fiscal_contrat: getValue('Regime_fiscal_contrat'),
        Montant_loyer_mensuel: getValue('Montant_loyer_mensuel'),
        Devise: getValue('Devise'),
        Periodicite_Reglement_id: this.getDynamicChoiceValue('Periodicite_Reglement_id'),
        Existence_avenant: getCheckboxValue('Existence_avenant'),
        bailleur: {
          Type_personne: this.getDynamicChoiceValue('Type_personne'),
          Raison_social: getValue('Raison_social'),
          Nom_Prenom_Representant: getValue('Nom_Prenom_Representant'),
          Domicille_siege_social_bailleur: getValue('Domicille_siege_social_bailleur'),
          NIU: getValue('NIU'),
          Telephone: getValue('Telephone'),
          Num_doc: getValue('Num_doc'),
          Date_delivrance_doc: getValue('Date_delivrance_doc'),
          Statut_bailleur: this.getDynamicChoiceValue('Statut_bailleur'),
          Banque: getValue('Banque'),
          RIB: getValue('RIB'),
          Intitule_compte: getValue('Intitule_compte'),
          ayants_droit: window.TableManagers.ayantsDroitManager?.collectData() || []
        },
        avenants: this.collectAvenants(),
        non_mandatements: window.TableManagers.nonMandatementManager?.collectData() || []
      },
      pieces_collectees: await this.collectPiecesCollectees()
    };
    return data;
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
      Ref_Avenant: getValue('reference_avenant_1'),
      Date_Signature: getValue('date_signature_avenant_1'),
      Date_effet: getValue('date_effet_avenant_1'),
      statut_visa_budgetaire_avenant: getCheckboxValue('statut_visa_budgetaire_avenant_1'),
      Ancien_bailleur: getValue('avenant_1_ancien_bailleurs_list'),
      Nouveau_bailleur: getValue('avenant_1_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: getValue('avenant_1_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: getValue('avenant_1_nouveaumontant_loyer_mensuel')
    };

    if (avenant1.Ref_Avenant) {
      avenants.push(avenant1);
    }

    // Avenant 2
    const avenant2 = {
      Ref_Avenant: getValue('reference_avenant_2'),
      Date_Signature: getValue('date_signature_avenant_2'),
      Date_effet: getValue('date_effet_avenant_2'),
      statut_visa_budgetaire_avenant: getCheckboxValue('statut_visa_budgetaire_avenant_2'),
      Ancien_bailleur: getValue('avenant_2_ancien_bailleurs_list'),
      Nouveau_bailleur: getValue('avenant_2_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: getValue('avenant_2_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: getValue('avenant_2_nouveaumontant_loyer_mensuel')
    };

    if (avenant2.Ref_Avenant) {
      avenants.push(avenant2);
    }

    return avenants;
  }

  // ✅ Collecter les pièces collectées avec conversion base64
  async collectPiecesCollectees() {
    const pieces = [];
    const rows = document.querySelectorAll('.piece-row');

    await Promise.all(
      Array.from(rows).map(async row => {
        const pieceId = row.dataset.pieceId;
        const checkbox = row.querySelector('.piece-checkbox');
        const nombreInput = row.querySelector('.piece-nombre');
        const filesInput = row.querySelector('.piece-files');

        if (checkbox?.checked) {
          const images = [];

          // Récupérer les images existantes (en mode edit)
          const existingImages = [];
          const $existingImageItems = $(row).find('.existing-image-item');
          $existingImageItems.each(function () {
            const imageId = $(this).find('.delete-image').data('image-id');
            if (imageId) {
              existingImages.push({
                id: imageId,
                existing: true // Marquer comme existante
              });
            }
          });
          console.log('images existente: ', existingImages);

          // Convertir les nouveaux fichiers en base64
          if (filesInput && filesInput.files.length > 0) {
            for (let i = 0; i < filesInput.files.length; i++) {
              const file = filesInput.files[i];

              try {
                const base64 = await fileToBase64(file);

                images.push({
                  filename: file.name,
                  content: base64,
                  content_type: file.type,
                  size: file.size
                });
              } catch (error) {
                console.error(`Erreur conversion fichier ${file.name}:`, error);
              }
            }
          } else {
            // ✅ Si pas de nouveaux fichiers, reprendre les existants
            images.push(...existingImages);
          }

          pieces.push({
            piece_id: parseInt(pieceId),
            statut: true,
            nombre: parseInt(nombreInput?.value || 1),
            images: images
          });
        }
      })
    );

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

    if (!data.immeuble.pays) {
      errors.push('Le pays est requis');
    }
    if (!data.immeuble.region) {
      errors.push('La région est requise');
    }
    if (!data.immeuble.departement) {
      errors.push('Le département est requis');
    }

    if (!data.immeuble.arrondissement) {
      errors.push("L'arrondissement est requis");
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
      showLoader(this.form);

      // Collecter les données
      const formData = await this.collectFormData();

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
      const url = this.isEditMode ? `/api/fiches/${this.ficheId}/update/` : '/api/fiches/create/';
      const method = this.isEditMode ? 'PUT' : 'POST';
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
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
    const params = new URLSearchParams({
      arrondissement_id: arrondissementId,
      ...(this.isEditMode && { edit_mode: 'true', fiche_id: this.ficheId })
    });
    let url = `/api/fiches/numero/?${params.toString()}`;
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        }
      });
      const result = await response.json();
      if (response.ok && result.success) {
        const numeroField = document.getElementById('Numero_fiche_de_collecte');
        if (numeroField) {
          numeroField.value = result.numero_collecte;
          showNotification('Numéro de fiche généré automatiquement', 'success');
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
        showNotification(result.error || 'Erreur lors de la génération du numéro', 'warning');
      }
    } catch (error) {
      console.error('❌ Erreur génération numéro:', error);
      showNotification('Erreur lors de la génération du numéro de fiche', 'danger');
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
      submitBtn.innerHTML = this.isEditMode
        ? '<i class="bx bx-edit"></i> Mettre à jour'
        : '<i class="bx bx-save"></i> Enregistrer';
      submitBtn.classList.add(this.isEditMode ? 'btn-warning' : 'btn-primary');
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

  // edit mode functions
  async loadFicheData() {
    try {
      showLoader();

      const response = await fetch(`/api/fiches/${this.ficheId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        }
      });

      const result = await response.json();

      if (response.ok && result.success) {
        await this.populateForm(result.data);
        console.log('datas :', result.data);
        showNotification('Données chargées avec succès', 'success');
      } else {
        this.showErrors(['Erreur lors du chargement des données']);
      }
    } catch (error) {
      console.error('Erreur chargement:', error);
      this.showErrors(['Erreur lors du chargement de la fiche']);
    } finally {
      this.hideLoader();
    }
  }

  // ✅ Remplir le formulaire avec les données
  async populateForm(data) {
    // Champs simples de la fiche
    this.setValue('Numero_fiche_de_collecte', data.Numero_fiche_de_collecte);
    this.setValue('Date_de_collecte', data.Date_de_collecte);

    // Agent (Select2)
    await this.setSelect2Value('responsable_collecte', data.agent_collecte_id, data.Agent?.nom);
    await this.setSelect2Value('matricule_responsable_collecte', data.matricule_agent, data.Agent?.matricule);

    // Immeuble
    if (data.immeuble) {
      this.setValue('Designation', data.immeuble.Designation);
      this.setValue('Date_Construction', data.immeuble.Date_Construction);
      this.setValue('Nombre_de_pieces', data.immeuble.Nombre_de_pieces);
      this.setValue('Superficie_louer', data.immeuble.Superficie_louer);
      this.setValue('observation', data.immeuble.observation);

      // Dynamic choices
      this.setDynamicChoice('type_construction_id', data.immeuble.type_construction_id);
      this.setDynamicChoice('type_location_id', data.immeuble.type_location_id);
      this.setDynamicChoice('statut_batisse_id', data.immeuble.statut_batisse_id);
      this.setDynamicChoice('revetement_int_id', data.immeuble.revetement_int_id);
      this.setDynamicChoice('revetement_ext_id', data.immeuble.revetement_ext_id);
      await this.setSelect2Value('pays', data.immeuble.pays_id, data.immeuble.pays?.libelle);
      this.setValue('Ville', data.immeuble.ville);
      this.setValue('Rue', data.immeuble.rue);
      await this.setSelect2Value('region', data.immeuble.region_id, data.immeuble.region?.libelle);
      await this.setSelect2Value('departement', data.immeuble.departement_id, data.immeuble.departement?.libelle);
      await this.setSelect2Value(
        'arrondissement',
        data.immeuble.arrondissement_id,
        data.immeuble.arrondissement?.libelle
      );
      this.setValue('Quartier', data.immeuble.quartier);
      this.setValue('Coordonee_gps', data.immeuble.coordonnees_gps);

      // Éléments de description
      if (data.immeuble.elements_description) {
        this.populateElementsDescription(data.immeuble.elements_description);
      }

      // Occupants
      if (data.immeuble.occupants_residents) {
        this.populateOccupants('logementsManager', data.immeuble.occupants_residents);
      }
      if (data.immeuble.occupants_bureaux) {
        this.populateOccupants('bureauxManager', data.immeuble.occupants_bureaux);
      }
    }

    // Contrat
    if (data.contrat) {
      this.setValue('Numero_contrat', data.contrat.Numero_contrat);
      this.setValue('Date_Signature_contrat', data.contrat.Date_Signature_contrat);
      this.setValue('Fonction_signataire_contrat', data.contrat.Fonction_signataire_contrat);
      this.setValue('Date_effet_contrat', data.contrat.Date_effet_contrat);
      this.setCheckboxValue('Existence_visa_budgétaire', data.contrat.Existence_visa_budgétaire);
      this.setValue('Duree_Contrat', data.contrat.Duree_Contrat);
      this.setCheckboxValue('Tacite_reconduction_contrat', data.contrat.Tacite_reconduction_contrat);
      this.setValue('Regime_fiscal_contrat', data.contrat.Regime_fiscal_contrat);
      this.setValue('Montant_loyer_mensuel', data.contrat.Montant_loyer_mensuel);
      this.setValue('Devise', data.contrat.Devise);

      this.setDynamicChoice('TypeContrat', data.contrat.TypeContrat);
      this.setDynamicChoice('Periodicite_Reglement_id', data.contrat.Periodicite_Reglement_id);
      this.setCheckboxValue('Existence_avenant', data.contrat.Existence_avenant);

      // Bailleur
      if (data.contrat.bailleur) {
        const bailleur = data.contrat.bailleur;
        this.setDynamicChoice('Type_personne', bailleur.Type_personne);
        this.setValue('Raison_social', bailleur.Raison_social);
        this.setValue('Nom_Prenom_Representant', bailleur.Nom_Prenom_Representant);
        this.setValue('Domicille_siege_social_bailleur', bailleur.Domicille_siege_social_bailleur);
        this.setValue('NIU', bailleur.NIU);
        this.setValue('Telephone', bailleur.Telephone);
        this.setValue('Num_doc', bailleur.Num_doc);
        this.setValue('Date_delivrance_doc', bailleur.Date_delivrance_doc);
        this.setDynamicChoice('Statut_bailleur', bailleur.Statut_bailleur);
        await this.setSelect2Value('Banque', bailleur.Banque);
        this.setValue('RIB', bailleur.RIB);
        this.setValue('Intitule_compte', bailleur.Intitule_compte);

        // Ayants droit
        if (bailleur.ayants_droit) {
          this.populateAyantsDroit(bailleur.ayants_droit);
        }
      }

      // Avenants
      if (data.contrat.avenants) {
        this.populateAvenants(data.contrat.avenants);
      }

      // Non-mandatements
      if (data.contrat.non_mandatements) {
        this.populateNonMandatements(data.contrat.non_mandatements);
      }
    }

    // Pièces collectées
    if (data.pieces_collectees) {
      this.populatePiecesCollectees(data.pieces_collectees);
    }
  }

  // ✅ Méthodes utilitaires pour remplir le formulaire
  setValue(fieldId, value) {
    const field = document.getElementById(fieldId);
    if (field && value !== null && value !== undefined) {
      field.value = value;
    }
  }

  setCheckboxValue(fieldId, value) {
    const checkbox = document.getElementById(fieldId);
    if (checkbox) {
      checkbox.checked = Boolean(value);
    }
  }

  setDynamicChoice(listId, value) {
    if (!value) return;

    const $list = document.getElementById(listId);
    if (!$list) return;

    const checkbox = $list.querySelector(`input[data-choice-id="${value}"]`);
    if (checkbox) {
      checkbox.checked = true;
    }
  }

  async setSelect2Value(selectId, value, text = null) {
    if (!value) return;

    const $select = $(`#${selectId}`);
    if (!$select.length) return;

    // Si le texte est fourni, créer l'option
    if (text) {
      const option = new Option(text, value, true, true);
      $select.append(option);
    } else {
      $select.val(value);
    }

    $select.trigger('change');
  }

  // ✅ Remplir les éléments de description
  populateElementsDescription(elements) {
    elements.forEach(element => {
      const $row = $(`tr[data-el-id="${element.element_id}"]`);
      if (!$row.length) return;

      // Cocher le bon checkbox
      if (element.statut === true) {
        $row.find(`#element_${element.element_id}_oui`).prop('checked', true);
        $row.find(`#nombre_input_${element.element_id}`).prop('disabled', false).val(element.nombre);
      } else if (element.statut === false) {
        $row.find(`#element_${element.element_id}_non`).prop('checked', true);
      }
    });
  }

  // ✅ Remplir les occupants (logements ou bureaux)
  populateOccupants(managerName, occupants) {
    const manager = window.TableManagers[managerName];

    if (!manager) {
      console.warn(`Manager ${managerName} non trouvé`);
      return;
    }

    if (!occupants || occupants.length === 0) {
      return;
    }

    // ✅ Mapping des noms de champs API vers les noms de champs du formulaire
    const fieldMapping = {
      // Pour les logements
      nom_prenom: 'Nom_Prenom_occupant_residence',
      administration_rattachement: 'Administration_rattachement',
      fonction: 'Fonction_occupant_residence',
      matricule: 'Matricule_occupant_residence',
      ref_acte: 'Ref_ActeJuridique_attribution',
      date_signature: 'Date_Signature_acte_juridique',

      // Pour les bureaux
      service_occupant_bureau: 'Service_occupant_bureau',
      administration_correspondante: 'Administration_correspondante',
      fonction_responsable: 'Fonction_occupant_bureau',
      date_signature_bureau: 'Date_signature_acte_attribution'
    };

    // Vider les lignes existantes
    if (manager.clearAllRows) {
      manager.clearAllRows();
    }

    occupants.forEach((occupant, index) => {
      const $row = manager.addNewRow();

      setTimeout(() => {
        Object.entries(occupant).forEach(([apiKey, value]) => {
          // ✅ Utiliser le mapping ou le nom original
          const formFieldName = fieldMapping[apiKey] || apiKey;
          const $field = $row.find(`[data-field="${formFieldName}"]`);

          if ($field.length) {
            if ($field.hasClass('select2-ajax')) {
              let optionId, optionText;

              if (typeof value === 'object' && value !== null) {
                optionId = value.id || value.value;
                optionText = value.text || value.label || value.libelle || optionId;
              } else {
                // Si c'est juste un ID, on l'utilise
                optionId = value;
                optionText = value;
              }

              if (optionId) {
                const option = new Option(optionText, optionId, true, true);
                $field.append(option).trigger('change');
              }
            } else {
              $field.val(value);
            }
          }
        });
      }, 200);
    });
  }

  // ✅ Remplir les ayants droit
  populateAyantsDroit(ayantsDroit) {
    const manager = window.TableManagers.ayantsDroitManager;
    if (!manager) return;

    // Vider les lignes existantes
    if (manager.clearAllRows) {
      manager.clearAllRows();
    }

    ayantsDroit.forEach(ayant => {
      const $row = manager.addNewRow();
      $row.find('[data-field="Nom_Prenom_ayant_droit"]').val(ayant.Nom_Prenom);
      $row.find('[data-field="Contact_ayant_droit"]').val(ayant.Contact);
      $row.find('[data-field="Reference_Grosse_ayant_droit"]').val(ayant.Ref_Grosse);
      $row.find('[data-field="Date_delivrance_grosse"]').val(ayant.Date_delivrance_Grosse);
      $row.find('[data-field="Reference_certificat_non_appel"]').val(ayant.Ref_Certificat_non_appel);
      $row.find('[data-field="Date_delivrance_certificat_non_appel"]').val(ayant.Date_delivrance_Certificat);
    });
  }

  // ✅ Remplir les avenants
  populateAvenants(avenants) {
    avenants.forEach(async (avenant, index) => {
      const num = index + 1;
      if (num > 2) return; // Maximum 2 avenants dans le formulaire

      this.setValue(`reference_avenant_${num}`, avenant.Ref_Avenant);
      this.setValue(`date_signature_avenant_${num}`, avenant.Date_Signature);
      this.setValue(`date_effet_avenant_${num}`, avenant.Date_effet);

      // Bailleurs
      await this.setSelect2Value(
        `avenant_${num}_ancien_bailleurs_list`,
        avenant.Ancien_bailleur,
        avenant.Ancien_bailleur_object?.libelle
      );
      await this.setSelect2Value(
        `avenant_${num}_nouveau_bailleurs_list`,
        avenant.Nouveau_bailleur,
        avenant.Nouveau_bailleur_object?.libelle
      );

      this.setValue(`avenant_${num}_ancienmontant_loyer_mensuel`, avenant.Montant_TTC_Mensuel_ancien);
      this.setValue(`avenant_${num}_nouveaumontant_loyer_mensuel`, avenant.Montant_TTC_Mensuel_Nouveau);
    });
  }

  // ✅ Remplir les non-mandatements
  populateNonMandatements(nonMandatements) {
    const manager = window.TableManagers.nonMandatementManager;
    if (!manager) return;

    // Vider les lignes existantes
    if (manager.clearAllRows) {
      manager.clearAllRows();
    }

    nonMandatements.forEach(nm => {
      const $row = manager.addNewRow();
      const rowId = $row.data('row-id');

      // Champs simples
      const $exercice = $row.find(`[name="nonmandatement_${rowId}_exercice"]`);
      if (nm.Exercice) {
        const option = new Option(nm.Exercice.libelle || nm.Exercice, nm.Exercice.id || nm.Exercice, true, true);
        $exercice.append(option).trigger('change');
      }

      $row.find(`[name="nonmandatement_${rowId}_loyer_mensuel"]`).val(nm.Loyer_Mensuel);
      $row.find(`[name="nonmandatement_${rowId}_reference"]`).val(nm.Ref_Attestattion);
      $row.find(`[name="nonmandatement_${rowId}_date_signature"]`).val(nm.Date_signature);
      $row.find(`[name="nonmandatement_${rowId}_montant_total"]`).val(nm.Montant_total_exercice);
      $row.find(`[name="nonmandatement_${rowId}_visa"]`).val(nm.Visa_budgétaire);
      $row.find(`[name="nonmandatement_${rowId}_reference_contrat"]`).val(nm.Ref_contrat_avenant);

      // Cocher les mois
      const moisMapping = [
        'janvier',
        'fevrier',
        'mars',
        'avril',
        'mai',
        'juin',
        'juillet',
        'aout',
        'septembre',
        'octobre',
        'novembre',
        'decembre'
      ];

      moisMapping.forEach((mois, index) => {
        if (nm[mois]) {
          $row.find(`[name="nonmandatement_${rowId}_mois_${index + 1}"]`).prop('checked', true);
        }
      });
    });
  }

  // ✅ Remplir les pièces collectées
  populatePiecesCollectees(pieces) {
    pieces.forEach(piece => {
      const $row = $(`.piece-row[data-piece-id="${piece.piece_id}"]`);
      if (!$row.length) return;

      // Cocher la checkbox
      const $checkbox = $row.find('.piece-checkbox');
      $checkbox.prop('checked', true);

      // Utiliser les MÊMES sélecteurs que dans initPiecesCollectees()
      const elementId = piece.piece_id;
      const $nombreInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $fileInput = $row.find(`#piece_image_input_${elementId}`);

      $nombreInput.prop('disabled', false).val(piece.nombre);
      $fileInput.prop('disabled', false);

      if (piece.images && piece.images.length > 0) {
        this.displayExistingImages($row, piece.images);
      }
    });
  }

  // ✅ Afficher les images existantes
  displayExistingImages($row, images) {
    const pieceId = $row.data('piece-id');
    const $imagesContainer = $row.find('.existing-images');

    if (!$imagesContainer.length) {
      $row.find('.piece-files').after('<div class="existing-images mt-2"></div>');
    }

    const imagesHtml = images
      .map(
        img => `
      <div class="existing-image-item d-inline-block me-2 mb-2 position-relative">
        <img src="${img.image}" alt="${img.legende || 'Image'}"
          class="img-thumbnail" style="width: 80px; height: 80px; object-fit: cover;">
        <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0 delete-image"
          data-image-id="${img.id}" style="padding: 2px 6px;">
          <i class="bx bx-x"></i>
        </button>
      </div>
    `
      )
      .join('');

    $row.find('.existing-images').html(`
      ${imagesHtml}
    `);

    // Gérer la suppression d'images
    $row.find('.delete-image').on('click', function () {
      const imageId = $(this).data('image-id');
      // Marquer pour suppression
      if (!window.imagesToDelete) {
        window.imagesToDelete = [];
      }
      window.imagesToDelete.push(imageId);
      $(this).closest('.existing-image-item').remove();
    });
  }
}

$(function () {
  // Récupérer l'ID de la fiche depuis l'URL ou un attribut data
  const urlParams = new URLSearchParams(window.location.search);
  const ficheId = urlParams.get('fiche_id') || $('#ficheCollecteForm').data('fiche-id');
  const formHandler = new FicheCollecteFormHandler('ficheCollecteForm', ficheId);
});
