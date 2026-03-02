/**
 * module de remplissage du formulaire
 */
export const FormPopulator = {
  // ✅ Méthodes utilitaires pour remplir le formulaire
  setValue(fieldId, value) {
    const field = document.getElementById(fieldId);
    if (field && value !== null && value !== undefined) {
      field.value = value;
    }
  },

  setCheckboxValue(fieldId, value) {
    const checkbox = document.getElementById(fieldId);
    if (checkbox) {
      checkbox.checked = Boolean(value);
    }
  },

  setDynamicChoice(listId, value) {
    if (!value) return;

    const $list = document.getElementById(listId);
    if (!$list) return;

    const checkbox = $list.querySelector(`input[data-choice-id="${value}"]`);
    if (checkbox) {
      checkbox.checked = true;
    }
  },

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
  },

  // ✅ Remplir les éléments de description
  populateElementsDescription(elements) {
    elements.forEach(element => {
      const $row = $(`tr[data-el-id="${element.element_id}"]`);
      if (!$row.length) return;

      // Cocher le bon checkbox
      if (element.statut === true) {
        $row.find(`#element_${element.element_id}_oui`).prop('checked', true);
        $row.find(`#element_${element.element_id}_non`).prop('checked', false);
        $row.find(`#nombre_input_${element.element_id}`).prop('disabled', false).val(element.nombre);
      } else if (element.statut === false) {
        $row.find(`#element_${element.element_id}_non`).prop('checked', true);
        $row.find(`#element_${element.element_id}_oui`).prop('checked', false);
      }
    });
  },

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
  },

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
  },

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
  },

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
      if (nm.statut_visa_budgetaire === true) {
        $row.find('[data-field="statut_visa_budgetaire_oui"]').prop('checked', true);
      } else if (nm.statut_visa_budgetaire === false) {
        $row.find('[data-field="statut_visa_budgetaire_non"]').prop('checked', true);
      }
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
  },

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
  },

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
  },

  // remplir les informations de l'immeuble
  async populateImmeubleDatas(immeuble) {
    // set hidden input value for id :
    this.setValue('immeuble_id', immeuble.id);

    // set simple input value :
    this.setValue('Designation', immeuble.Designation);
    this.setValue('Date_Construction', immeuble.Date_Construction);
    this.setValue('Nombre_de_pieces', immeuble.Nombre_de_pieces);
    this.setValue('Superficie_louer', immeuble.Superficie_louer);
    this.setValue('observation', immeuble.observation);

    // Dynamic choices
    this.setDynamicChoice('type_construction_id', immeuble.type_construction_id);
    this.setDynamicChoice('type_location_id', immeuble.type_location_id);
    this.setDynamicChoice('statut_batisse_id', immeuble.statut_batisse_id);
    this.setDynamicChoice('revetement_int_id', immeuble.revetement_int_id);
    this.setDynamicChoice('revetement_ext_id', immeuble.revetement_ext_id);
    await this.setSelect2Value('pays', immeuble.pays_id, immeuble.pays?.libelle);
    this.setValue('Ville', immeuble.ville);
    this.setValue('Rue', immeuble.rue);
    await this.setSelect2Value('region', immeuble.region_id, immeuble.region?.libelle);
    await this.setSelect2Value('departement', immeuble.departement_id, immeuble.departement?.libelle);
    await this.setSelect2Value('arrondissement', immeuble.arrondissement_id, immeuble.arrondissement?.libelle);
    this.setValue('Quartier', immeuble.quartier);
    this.setValue('Coordonee_gps', immeuble.coordonnees_gps);

    // Éléments de description
    if (immeuble.elements_description) {
      this.populateElementsDescription(immeuble.elements_description);
    }

    // Occupants
    if (immeuble.occupants_residents) {
      this.populateOccupants('logementsManager', immeuble.occupants_residents);
    }
    if (immeuble.occupants_bureaux) {
      this.populateOccupants('bureauxManager', immeuble.occupants_bureaux);
    }
  }
};
