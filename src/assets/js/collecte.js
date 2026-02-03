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
  }

  // Collecter toutes les données du formulaire
  collectFormData() {
    // Vérifier que les managers sont disponibles
    if (!window.TableManagers) {
      console.error('TableManagers not initialized');
      throw new Error('Les gestionnaires de tableaux ne sont pas initialisés');
    }
    return {
      // Champs de la fiche
      Numero_fiche_de_collecte: this.getValue('Numero_fiche_de_collecte'),
      agent_collecte_id: this.getValue('responsable_collecte'),
      matricule_agent: this.getValue('matricule_responsable_collecte'),
      Date_de_collecte: this.getValue('Date_de_collecte'),

      // Immeuble
      immeuble: {
        Designation: this.getValue('Designation'),
        Construction: this.getValue('construction_choice_hidden'),
        Type_location: this.getValue('type_location_choice_hidden'),
        Date_Construction: this.getValue('Date_Construction'),
        Nombre_de_pieces: this.getValue('Nombre_de_pieces'),
        Superficie_louer: this.getValue('Superficie_louer'),
        Situation_de_la_batisse: this.getValue('statut_choice_hidden'),
        Revetement_interieure: this.getValue('revetementinterieure_choice_hidden'),
        Revetement_exterieure: this.getValue('revetementexterieure_choice_hidden'),
        observation: this.getValue('observation'),

        // Localisation
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

        // Éléments de description
        elements_description: this.collectElementsDescription(),

        // Occupants
        occupants_residents: window.TableManagers.logementsManager?.collectData() || [],
        occupants_bureaux: window.TableManagers.bureauxManager?.collectData() || []
      },

      // Contrat
      contrat: {
        TypeContrat: this.getValue('typecontrat_choice_hidden'),
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
        periodicite_reglement_id: this.getValue('periodicitereglement_choice_hidden'),
        Existence_avenant: this.getCheckboxValue('Existence_avenant'),

        // Bailleur
        bailleur: {
          Type_personne: this.getValue('types_personnes_choice_hidden'),
          Raison_social: this.getValue('Raison_social'),
          Nom_Prenom_Representant: this.getValue('Nom_Prenom_Representant'),
          Domicille_siege_social_bailleur: this.getValue('Domicille_siege_social_bailleur'),
          NIU: this.getValue('NIU'),
          Telephone: this.getValue('Telephone'),
          Num_doc: this.getValue('Num_doc'),
          Date_delivrance_doc: this.getValue('Date_delivrance_doc'),
          Statut_bailleur: this.getValue('statut_bailleur_choice_hidden'),
          Banque: this.getValue('Banque'),
          RIB: this.getValue('RIB'),
          Intitule_compte: this.getValue('Intitule_compte'),

          // Ayants droit
          ayants_droit: window.TableManagers.ayantsDroitManager?.collectData() || []
        },

        // Avenants
        avenants: this.collectAvenants(),

        // Non-mandatements
        non_mandatements: window.TableManagers.nonMandatementManager?.collectData() || []
      },

      // Pièces collectées
      pieces_collectees: this.collectPiecesCollectees()
    };
  }

  getValue(fieldId) {
    const field = document.getElementById(fieldId);
    return field ? field.value : null;
  }

  getCheckboxValue(fieldId) {
    const checkbox = document.getElementById(fieldId);
    return checkbox ? checkbox.checked : false;
  }

  // Collecter les éléments de description
  collectElementsDescription() {
    const elements = [];
    document.querySelectorAll('.elements-collecte-container-tbody tr').forEach(row => {
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
      reference: this.getValue('reference_avenant_1'),
      date_signature: this.getValue('date_signature_avenant_1'),
      date_effet: this.getValue('date_effet_avenant_1'),
      ancien_bailleur_id: this.getValue('avenant_1_ancien_bailleurs_list'),
      nouveau_bailleur_id: this.getValue('avenant_1_nouveau_bailleurs_list'),
      ancien_loyer_mensuel: this.getValue('avenant_1_ancienmontant_loyer_mensuel'),
      nouveau_loyer_mensuel: this.getValue('avenant_1_nouveaumontant_loyer_mensuel')
    };

    if (avenant1.reference) {
      avenants.push(avenant1);
    }

    // Avenant 2
    const avenant2 = {
      reference: this.getValue('reference_avenant_2'),
      date_signature: this.getValue('date_signature_avenant_2'),
      date_effet: this.getValue('date_effet_avenant_2'),
      ancien_bailleur_id: this.getValue('avenant_2_ancien_bailleurs_list'),
      nouveau_bailleur_id: this.getValue('avenant_2_nouveau_bailleurs_list'),
      ancien_loyer_mensuel: this.getValue('avenant_2_ancienmontant_loyer_mensuel'),
      nouveau_loyer_mensuel: this.getValue('avenant_2_nouveaumontant_loyer_mensuel')
    };

    if (avenant2.reference) {
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

    if (!data.immeuble.Construction) {
      errors.push('Le type de construction est requis');
    }

    if (!data.contrat.Numero_contrat) {
      errors.push('Le numéro de contrat est requis');
    }

    if (!data.contrat.bailleur.Raison_social) {
      errors.push('Le nom du bailleur est requis');
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
        this.showSuccess(result.message, result.fiche_id);
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
    const customMessages = {
      // Erreurs par champ spécifique
      'immeuble.type_construction_id': 'Veuillez sélectionner un type de construction',
      'immeuble.type_location_id': 'Veuillez sélectionner un type de location',
      'immeuble.statut_batisse_id': 'Veuillez sélectionner un statut de bâtisse',
      'immeuble.revetement_int_id': 'Veuillez sélectionner un type de revêtement intérieur',
      'immeuble.revetement_ext_id': 'Veuillez sélectionner un type de revêtement extérieur',
      'immeuble.Designation': 'Veuillez saisir la désignation du bien',
      'contrat.bailleur.Type_personne': 'Veuillez sélectionner le type de personne du bailleur',
      'contrat.Duree_Contrat': 'Veuillez saisir la durée du contrat'
    };

    // Si un message personnalisé existe pour ce champ
    if (customMessages[field]) {
      return customMessages[field];
    }

    // Sinon, traduire les messages génériques
    const genericMessages = {
      'Un nombre entier valide est requis.': 'Veuillez sélectionner une option valide',
      'Ce champ est obligatoire.': 'Ce champ est requis',
      'This field is required.': 'Ce champ est requis',
      'A valid integer is required.': 'Veuillez sélectionner une option valide',
      'Enter a valid email address.': 'Veuillez saisir une adresse email valide'
    };

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

  // Utilitaires
  getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  }

  showLoader() {
    // Afficher un spinner ou désactiver le bouton
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Enregistrement...';
    }
  }

  hideLoader() {
    const submitBtn = this.form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = 'Enregistrer';
    }
  }

  showSuccess(message, ficheId) {
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
      window.location.href = `/collecte/${ficheId}/`;
    }, 3000);
  }
}

$(function () {
  // there the form validation and submission
  const formHandler = new FicheCollecteFormHandler('ficheCollecteForm');
});
