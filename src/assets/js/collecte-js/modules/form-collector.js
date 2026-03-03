/**
 * Collectes des données
 */
import { FormUtils } from './form-utils.js';
import { tableManagers } from '../config.js';
export const Collectors = {
  // Collecter les éléments de description uniquement ceux qui sont à oui
  collectElementsDescription(containerClass = '.main-elements-immeuble-container') {
    const elements = [];
    document.querySelectorAll(`${containerClass}-tbody tr`).forEach(row => {
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

  // collecter les informations de immeuble:
  async collectImmeubleDatas(prefix = 'main') {
    return {
      Designation: FormUtils.getValue(`${prefix}_Designation`),
      type_construction_id: FormUtils.getDynamicChoiceValue(`${prefix}_type_construction_id`),
      type_location_id: FormUtils.getDynamicChoiceValue(`${prefix}_type_location_id`),
      Date_Construction: FormUtils.getValue(`${prefix}_Date_Construction`),
      Nombre_de_pieces: FormUtils.getValue(`${prefix}_Nombre_de_pieces`),
      Superficie_louer: FormUtils.getValue(`${prefix}_Superficie_louer`),
      statut_batisse_id: FormUtils.getDynamicChoiceValue(`${prefix}_statut_batisse_id`),
      revetement_int_id: FormUtils.getDynamicChoiceValue(`${prefix}_revetement_int_id`),
      revetement_ext_id: FormUtils.getDynamicChoiceValue(`${prefix}_revetement_ext_id`),
      observation: FormUtils.getValue(`${prefix}_observation`),
      pays: FormUtils.getValue(`${prefix}_pays`),
      Ville: FormUtils.getValue(`${prefix}_Ville`),
      Rue: FormUtils.getValue(`${prefix}_Rue`),
      region: FormUtils.getValue(`${prefix}_region`),
      departement: FormUtils.getValue(`${prefix}_departement`),
      arrondissement: FormUtils.getValue(`${prefix}_arrondissement`),
      Quartier: FormUtils.getValue(`${prefix}_Quartier`),
      Coordonee_gps: FormUtils.getValue(`${prefix}_Coordonee_gps`),
      elements_description: await this.collectElementsDescription(),
      occupants_residents: (await tableManagers.logementsManager?.collectData()) || [],
      occupants_bureaux: (await tableManagers.bureauxManager?.collectData()) || []
    };
  },

  // collecter les informations de bailleur:
  async collectBailleurDatas() {
    return {
      Type_personne: FormUtils.getDynamicChoiceValue('main_Type_personne'),
      Raison_social: FormUtils.getValue('main_Raison_social'),
      Nom_Prenom_Representant: FormUtils.getValue('main_Nom_Prenom_Representant'),
      Domicille_siege_social_bailleur: FormUtils.getValue('main_Domicille_siege_social_bailleur'),
      NIU: FormUtils.getValue('main_NIU'),
      Telephone: FormUtils.getValue('main_Telephone'),
      Num_doc: FormUtils.getValue('main_Num_doc'),
      Date_delivrance_doc: FormUtils.getValue('main_Date_delivrance_doc'),
      Statut_bailleur: FormUtils.getDynamicChoiceValue('main_Statut_bailleur'),
      Role_bailleur: FormUtils.getDynamicChoiceValue('main_Role_bailleur'),
      Banque: FormUtils.getValue('main_Banque'),
      RIB: FormUtils.getValue('main_RIB'),
      Intitule_compte: FormUtils.getValue('main_Intitule_compte'),
      ayants_droit: (await tableManagers.ayantsDroitManager.collectData()) || []
    };
  },

  // collecter les informations de immeuble:
  async collectContratDatas() {
    return {
      TypeContrat: FormUtils.getDynamicChoiceValue('TypeContrat'),
      Numero_contrat: FormUtils.getValue('Numero_contrat'),
      Date_Signature_contrat: FormUtils.getValue('Date_Signature_contrat'),
      Fonction_signataire_contrat: FormUtils.getValue('Fonction_signataire_contrat'),
      Date_effet_contrat: FormUtils.getValue('Date_effet_contrat'),
      Existence_visa_budgétaire: FormUtils.getCheckboxValueYesNo('Existence_visa_budgétaire'),
      Duree_Contrat: FormUtils.getValue('Duree_Contrat'),
      Tacite_reconduction_contrat: FormUtils.getCheckboxValueYesNo('Tacite_reconduction_contrat'),
      Regime_fiscal_contrat: FormUtils.getValue('Regime_fiscal_contrat'),
      Montant_loyer_mensuel: FormUtils.getValue('Montant_loyer_mensuel'),
      Devise: FormUtils.getValue('Devise'),
      Periodicite_Reglement_id: FormUtils.getDynamicChoiceValue('Periodicite_Reglement_id'),
      Existence_avenant: FormUtils.getCheckboxValueYesNo('Existence_avenant'),
      bailleur: await this.collectBailleurDatas(),
      avenants: await this.collectAvenants(),
      non_mandatements: (await tableManagers.nonMandatementManager.collectData()) || []
    };
  }
};
