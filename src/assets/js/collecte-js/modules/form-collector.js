/**
 * Collectes des données
 */
import { FormUtils } from './form-utils.js';
export const Collectors = {
  // Collecter les éléments de description uniquement ceux qui sont à oui
  collectElementsDescription() {
    const elements = [];
    document.querySelectorAll('.elements-immeuble-container-tbody tr').forEach(row => {
      const elementId = row.dataset.elId;
      const ouiChecked = row.querySelector(`#element_${elementId}_oui`)?.checked;
      const nombre = row.querySelector(`input[type="number"]`)?.value || 0;

      if (ouiChecked) {
        elements.push({
          element_id: parseInt(elementId),
          statut: ouiChecked,
          nombre: parseInt(nombre)
        });
      }
    });
    return elements;
  },

  // Collecter les avenants
  collectAvenants() {
    const avenants = [];

    // Avenant 1
    const avenant1 = {
      Ref_Avenant: FormUtils.getValue('reference_avenant_1'),
      Date_Signature: FormUtils.getValue('date_signature_avenant_1'),
      Date_effet: FormUtils.getValue('date_effet_avenant_1'),
      statut_visa_budgetaire_avenant: FormUtils.getCheckboxValueYesNo('statut_visa_budgetaire_avenant_1'),
      Ancien_bailleur: FormUtils.getValue('avenant_1_ancien_bailleurs_list'),
      Nouveau_bailleur: FormUtils.getValue('avenant_1_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: FormUtils.getValue('avenant_1_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: FormUtils.getValue('avenant_1_nouveaumontant_loyer_mensuel')
    };

    if (avenant1.Ref_Avenant) {
      avenants.push(avenant1);
    }

    // Avenant 2
    const avenant2 = {
      Ref_Avenant: FormUtils.getValue('reference_avenant_2'),
      Date_Signature: FormUtils.getValue('date_signature_avenant_2'),
      Date_effet: FormUtils.getValue('date_effet_avenant_2'),
      statut_visa_budgetaire_avenant: FormUtils.getCheckboxValueYesNo('statut_visa_budgetaire_avenant_2'),
      Ancien_bailleur: FormUtils.getValue('avenant_2_ancien_bailleurs_list'),
      Nouveau_bailleur: FormUtils.getValue('avenant_2_nouveau_bailleurs_list'),
      Montant_TTC_Mensuel_ancien: FormUtils.getValue('avenant_2_ancienmontant_loyer_mensuel'),
      Montant_TTC_Mensuel_Nouveau: FormUtils.getValue('avenant_2_nouveaumontant_loyer_mensuel')
    };

    if (avenant2.Ref_Avenant) {
      avenants.push(avenant2);
    }

    return avenants;
  },

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
                const base64 = await FormUtils.fileToBase64(file);

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
  },

  // collecter informations de immeuble:
  async collectImmeubleDatas() {
    return {
      Designation: FormUtils.getValue('Designation'),
      type_construction_id: FormUtils.getDynamicChoiceValue('type_construction_id'),
      type_location_id: FormUtils.getDynamicChoiceValue('type_location_id'),
      Date_Construction: FormUtils.getValue('Date_Construction'),
      Nombre_de_pieces: FormUtils.getValue('Nombre_de_pieces'),
      Superficie_louer: FormUtils.getValue('Superficie_louer'),
      statut_batisse_id: FormUtils.getDynamicChoiceValue('statut_batisse_id'),
      revetement_int_id: FormUtils.getDynamicChoiceValue('revetement_int_id'),
      revetement_ext_id: FormUtils.getDynamicChoiceValue('revetement_ext_id'),
      observation: FormUtils.getValue('observation'),
      pays: FormUtils.getValue('pays'),
      Ville: FormUtils.getValue('Ville'),
      Rue: FormUtils.getValue('Rue'),
      region: FormUtils.getValue('region'),
      departement: FormUtils.getValue('departement'),
      arrondissement: FormUtils.getValue('arrondissement'),
      Quartier: FormUtils.getValue('Quartier'),
      Coordonee_gps: FormUtils.getValue('Coordonee_gps'),
      elements_description: Collectors.collectElementsDescription(),
      occupants_residents: window.TableManagers.logementsManager?.collectData() || [],
      occupants_bureaux: window.TableManagers.bureauxManager?.collectData() || []
    };
  }
};
