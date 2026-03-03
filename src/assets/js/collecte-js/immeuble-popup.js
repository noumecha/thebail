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
  modalId: '#update-immeuble-modal',
  formId: '#update-immeuble-form',
  method: 'PUT',

  onOpen: $modal => {
    FormUtils.initSelect2Ajax($modal);
    FormUtils.initElementsImmeuble('#popup-elements-immeuble-container');
    const toggleConfigs = [
      { listId: 'update-immeuble-modal_type_construction_id', hiddenId: 'type_construction_id_choice_hidden' },
      { listId: 'update-immeuble-modal_type_location_id', hiddenId: 'type_location_id_choice_hidden' },
      { listId: 'update-immeuble-modal_statut_batisse_id', hiddenId: 'statut_batisse_id_choice_hidden' },
      { listId: 'update-immeuble-modal_revetement_int_id', hiddenId: 'revetement_int_id_choice_hidden' },
      { listId: 'update-immeuble-modal_revetement_ext_id', hiddenId: 'revetement_ext_id_choice_hidden' }
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
  },

  onClose: $modal => {
    $modal.find('.select2-ajax').each(function () {
      if ($(this).hasClass('select2-hidden-accessible')) {
        $(this).select2('destroy');
      }
    });
  },

  onSuccess: (result, mainListId) => {
    resetForm($('#update-immeuble-modal'));
    $('#update-immeuble-modal').modal('hide');
    const newOption = new Option(result.data?.bailleur, result.data?.bailleur_id, true, true);
    console.log('main list id : ', mainListId);
    $(mainListId).append(newOption).trigger('change');
  },

  collectFormData: async () => {
    const prefix = 'update-immeuble-modal';
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
