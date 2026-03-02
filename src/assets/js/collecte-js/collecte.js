// collecte.js
import { FormUtils } from './modules/form-utils.js';
import { Validators } from './modules/form-validator.js';
import { Collectors } from './modules/form-collector.js';
import { FormPopulator } from './modules/form-populator.js';
import { APIUtils } from './modules/api-utils.js';

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
    FormUtils.initElementsImmeuble();
    FormUtils.initPiecesCollectees();
    // mode :
    if (this.isEditMode) {
      await this.loadFicheData();
    }
    // generate numero collecte
    $('#arrondissement').on('select2:select', e => {
      const arrondissementId = e.params.data.id;
      if (arrondissementId) {
        APIUtils.generateFicheCollecte(arrondissementId);
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

  // Collecter toutes les données du formulaire
  async collectFormData() {
    // Vérifier que les managers sont disponibles
    if (!window.TableManagers) {
      console.error('TableManagers not initialized');
      throw new Error('Les gestionnaires de tableaux ne sont pas initialisés');
    }
    const data = {
      Numero_fiche_de_collecte: FormUtils.getValue('Numero_fiche_de_collecte'),
      agent_collecte_id: FormUtils.getValue('responsable_collecte'),
      matricule_agent: FormUtils.getValue('matricule_responsable_collecte'),
      Date_de_collecte: FormUtils.getValue('Date_de_collecte'),
      immeuble: {
        Designation: FormUtils.getValue('Designation'),
        immeuble_id: FormUtils.getValue('immeuble_id'),
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
      },
      contrat: {
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
        bailleur: {
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
          ayants_droit: window.TableManagers.ayantsDroitManager?.collectData() || []
        },
        avenants: Collectors.collectAvenants(),
        non_mandatements: window.TableManagers.nonMandatementManager?.collectData() || []
      },
      pieces_collectees: await Collectors.collectPiecesCollectees()
    };
    return data;
  }

  // Soumettre le formulaire
  async handleSubmit() {
    try {
      // Afficher un loader
      FormUtils.showLoader(this.form);

      // Collecter les données
      const formData = await this.collectFormData();

      // ✅ DEBUG : Afficher les données avant envoi
      console.log('📤 Données envoyées:', JSON.stringify(formData, null, 2));

      // Valider les données
      const errors = Validators.validateData(formData);
      if (errors.length > 0) {
        FormUtils.showErrors(errors, this.form);
        FormUtils.hideLoader(this.form);
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
        FormUtils.showSuccess(result.message, this.form);
      } else {
        FormUtils.showErrors([result.message || 'Erreur lors de la soumission'], this.form);
        FormUtils.handleServerErrors(result, this.form);
        console.error('Erreurs de validation:', result.errors);
      }
    } catch (error) {
      console.error('Erreur:', error);
      FormUtils.showErrors(['Une erreur est survenue lors de la soumission'], this.form);
    } finally {
      FormUtils.hideLoader(this.form);
    }
  }

  // edit mode functions
  async loadFicheData() {
    try {
      FormUtils.showLoader();

      const response = await fetch(`/api/fiches/${this.ficheId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        }
      });

      const result = await response.json();

      if (response.ok && result.success) {
        console.log('datas :', result.data);
        await this.populateForm(result.data);
        showNotification('Données chargées avec succès', 'success');
      } else {
        FormUtils.showErrors(['Erreur lors du chargement des données'], this.form);
      }
    } catch (error) {
      console.error('Erreur chargement:', error);
      FormUtils.showErrors(['Erreur lors du chargement de la fiche'], this.form);
    } finally {
      FormUtils.hideLoader(this.form);
    }
  }

  // ✅ Remplir le formulaire avec les données
  async populateForm(data) {
    // Champs simples de la fiche
    FormPopulator.setValue('Numero_fiche_de_collecte', data.Numero_fiche_de_collecte);
    FormPopulator.setValue('Date_de_collecte', data.Date_de_collecte);

    // Agent (Select2)
    await FormPopulator.setSelect2Value('responsable_collecte', data.agent_collecte_id, data.Agent?.nom);
    await FormPopulator.setSelect2Value('matricule_responsable_collecte', data.matricule_agent, data.Agent?.matricule);

    // Immeuble
    if (data.immeuble) {
      FormPopulator.setValue('Designation', data.immeuble.Designation);
      FormPopulator.setValue('Date_Construction', data.immeuble.Date_Construction);
      FormPopulator.setValue('Nombre_de_pieces', data.immeuble.Nombre_de_pieces);
      FormPopulator.setValue('Superficie_louer', data.immeuble.Superficie_louer);
      FormPopulator.setValue('observation', data.immeuble.observation);

      // Dynamic choices
      FormPopulator.setDynamicChoice('type_construction_id', data.immeuble.type_construction_id);
      FormPopulator.setDynamicChoice('type_location_id', data.immeuble.type_location_id);
      FormPopulator.setDynamicChoice('statut_batisse_id', data.immeuble.statut_batisse_id);
      FormPopulator.setDynamicChoice('revetement_int_id', data.immeuble.revetement_int_id);
      FormPopulator.setDynamicChoice('revetement_ext_id', data.immeuble.revetement_ext_id);
      await FormPopulator.setSelect2Value('pays', data.immeuble.pays_id, data.immeuble.pays?.libelle);
      FormPopulator.setValue('Ville', data.immeuble.ville);
      FormPopulator.setValue('Rue', data.immeuble.rue);
      await FormPopulator.setSelect2Value('region', data.immeuble.region_id, data.immeuble.region?.libelle);
      await FormPopulator.setSelect2Value(
        'departement',
        data.immeuble.departement_id,
        data.immeuble.departement?.libelle
      );
      await FormPopulator.setSelect2Value(
        'arrondissement',
        data.immeuble.arrondissement_id,
        data.immeuble.arrondissement?.libelle
      );
      FormPopulator.setValue('Quartier', data.immeuble.quartier);
      FormPopulator.setValue('Coordonee_gps', data.immeuble.coordonnees_gps);

      // Éléments de description
      if (data.immeuble.elements_description) {
        FormPopulator.populateElementsDescription(data.immeuble.elements_description);
      }

      // Occupants
      if (data.immeuble.occupants_residents) {
        FormPopulator.populateOccupants('logementsManager', data.immeuble.occupants_residents);
      }
      if (data.immeuble.occupants_bureaux) {
        FormPopulator.populateOccupants('bureauxManager', data.immeuble.occupants_bureaux);
      }
    }

    // Contrat
    if (data.contrat) {
      FormPopulator.setValue('Numero_contrat', data.contrat.Numero_contrat);
      FormPopulator.setValue('Date_Signature_contrat', data.contrat.Date_Signature_contrat);
      FormPopulator.setValue('Fonction_signataire_contrat', data.contrat.Fonction_signataire_contrat);
      FormPopulator.setValue('Date_effet_contrat', data.contrat.Date_effet_contrat);
      FormPopulator.setCheckboxValue('Existence_visa_budgétaire', data.contrat.Existence_visa_budgétaire);
      FormPopulator.setValue('Duree_Contrat', data.contrat.Duree_Contrat);
      FormPopulator.setCheckboxValue('Tacite_reconduction_contrat', data.contrat.Tacite_reconduction_contrat);
      FormPopulator.setValue('Regime_fiscal_contrat', data.contrat.Regime_fiscal_contrat);
      FormPopulator.setValue('Montant_loyer_mensuel', data.contrat.Montant_loyer_mensuel);
      FormPopulator.setValue('Devise', data.contrat.Devise);

      FormPopulator.setDynamicChoice('TypeContrat', data.contrat.TypeContrat);
      FormPopulator.setDynamicChoice('Periodicite_Reglement_id', data.contrat.Periodicite_Reglement_id);
      FormPopulator.setCheckboxValue('Existence_avenant', data.contrat.Existence_avenant);

      // Bailleur
      if (data.contrat.bailleur) {
        const bailleur = data.contrat.bailleur;
        FormPopulator.setDynamicChoice('Type_personne', bailleur.Type_personne);
        FormPopulator.setValue('Raison_social', bailleur.Raison_social);
        FormPopulator.setValue('Nom_Prenom_Representant', bailleur.Nom_Prenom_Representant);
        FormPopulator.setValue('Domicille_siege_social_bailleur', bailleur.Domicille_siege_social_bailleur);
        FormPopulator.setValue('NIU', bailleur.NIU);
        FormPopulator.setValue('Telephone', bailleur.Telephone);
        FormPopulator.setValue('Num_doc', bailleur.Num_doc);
        FormPopulator.setValue('Date_delivrance_doc', bailleur.Date_delivrance_doc);
        FormPopulator.setDynamicChoice('Statut_bailleur', bailleur.Statut_bailleur);
        await FormPopulator.setSelect2Value('Banque', bailleur.Banque);
        FormPopulator.setValue('RIB', bailleur.RIB);
        FormPopulator.setValue('Intitule_compte', bailleur.Intitule_compte);

        // Ayants droit
        if (bailleur.ayants_droit) {
          FormPopulator.populateAyantsDroit(bailleur.ayants_droit);
        }
      }

      // Avenants
      if (data.contrat.avenants) {
        FormPopulator.populateAvenants(data.contrat.avenants);
      }

      // Non-mandatements
      if (data.contrat.non_mandatements) {
        FormPopulator.populateNonMandatements(data.contrat.non_mandatements);
      }
    }

    // Pièces collectées
    if (data.pieces_collectees) {
      FormPopulator.populatePiecesCollectees(data.pieces_collectees);
    }
  }
}

$(function () {
  // Récupérer l'ID de la fiche depuis l'URL ou un attribut data
  const urlParams = new URLSearchParams(window.location.search);
  const ficheId = urlParams.get('fiche_id') || $('#ficheCollecteForm').data('fiche-id');
  const formHandler = new FicheCollecteFormHandler('ficheCollecteForm', ficheId);
});
