/**
 * form manage popup modals
 */
import { ModalManager } from './modules/modal-manager.js';
import { FormUtils } from './modules/form-utils.js';
import { bindStatutRoleDependency } from './modules/dependencies.js';

/**
 * function to reset form
 * @return void
 */
function resetForm($modal) {
  // reset the form
  $modal.find('form')[0].reset();
  // reset hidden inputs for dynamic choices
  $modal.find('input[type="hidden"]').val('');
  // reset checkboxes
  $modal.find('.dynamic-check').prop('checked', false).trigger('change');
}

new ModalManager({
  modalId: '#create-bailleur-modal',
  formId: '#bailleur-form',

  onOpen: $modal => {
    FormUtils.initSelect2Ajax($modal);
    const toggleConfigs = [
      { listId: 'create-bailleur-modal_Type_personne', hiddenId: 'types_personnes_choice_hidden' },
      { listId: 'create-bailleur-modal_Statut_bailleur', hiddenId: 'statut_bailleur_choice_hidden' },
      { listId: 'create-bailleur-modal_Role_bailleur', hiddenId: 'role_bailleur_choice_hidden' }
    ];
    toggleConfigs.forEach(({ listId, hiddenId }) => {
      $modal.find('#' + listId).on('change', '.dynamic-check', function () {
        FormUtils.toggleCheck({
          listId,
          checkbox: this,
          dynamicCheckClass: 'dynamic-check',
          dynamicOptionClass: 'dynamic-option',
          dynamicInputClass: 'dynamic-x-input',
          hiddenId
        });
      });
    });
    // disabled an enable Role_bailleur base on Statut_bailleur checked or no
    bindStatutRoleDependency('#create-bailleur-modal_Statut_bailleur', '#create-bailleur-modal_Role_bailleur');
  },

  onClose: $modal => {
    $modal.find('.select2-ajax').each(function () {
      if ($(this).hasClass('select2-hidden-accessible')) {
        $(this).select2('destroy');
      }
    });
    resetForm($modal);
  },

  onSuccess: (result, mainListId) => {
    resetForm($('#create-bailleur-modal'));
    $('#create-bailleur-modal').modal('hide');
    const newOption = new Option(result.data?.bailleur, result.data?.bailleur_id, true, true);
    console.log('main list id : ', mainListId);
    $(mainListId).append(newOption).trigger('change');
  },

  collectFormData: async () => {
    const prefix = 'create-bailleur-modal';
    return {
      Type_personne: FormUtils.getDynamicChoiceValue(`${prefix}_Type_personne`),
      Raison_social: FormUtils.getValue(`${prefix}_Raison_social`),
      Nom_Prenom_Representant: FormUtils.getValue(`${prefix}_Nom_Prenom_Representant`),
      Domicille_siege_social_bailleur: FormUtils.getValue(`${prefix}_Domicille_siege_social_bailleur`),
      NIU: FormUtils.getValue(`${prefix}_NIU`),
      Telephone: FormUtils.getValue(`${prefix}_Telephone`),
      Num_doc: FormUtils.getValue(`${prefix}_Num_doc`),
      Date_delivrance_doc: FormUtils.getValue(`${prefix}_Date_delivrance_doc`),
      Statut_bailleur: FormUtils.getDynamicChoiceValue(`${prefix}_Statut_bailleur`),
      Role_bailleur: FormUtils.getDynamicChoiceValue(`${prefix}_Role_bailleur`),
      Banque: FormUtils.getValue(`${prefix}_Banque`),
      RIB: FormUtils.getValue(`${prefix}_RIB`),
      Intitule_compte: FormUtils.getValue(`${prefix}_Intitule_compte`)
    };
  }
});
