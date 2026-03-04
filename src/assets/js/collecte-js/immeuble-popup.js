/**
 * form manage popup modals
 */
import { ModalManager } from './modules/modal-manager.js';
import { FormUtils } from './modules/form-utils.js';
import { FormPopulator } from './modules/form-populator.js';
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

  onOpen: async $modal => {
    FormUtils.initSelect2Ajax($modal);
    await FormPopulator.reloadElements('#popup-elements-immeuble-container');
    FormUtils.initElementsImmeuble('#popup-elements-immeuble-container');
    // adding elements dynamically configuration
    const dynamic_choices_list_objects = [
      {
        listId: 'update-immeuble-modal_type_construction_id',
        hiddenId: 'update-immeuble-modal_type_construction_id-construction_choice_hidden',
        newInputId: 'update-immeuble-modal_type_construction_id-new_construction_input',
        formWrapper: 'update-immeuble-modal_type_construction_id-new_construction_wrapper',
        addButtonId: 'update-immeuble-modal_type_construction_id-add_construction_btn',
        ajaxUrl: '/add-choice/'
      },
      {
        listId: 'update-immeuble-modal_type_location_id',
        hiddenId: 'update-immeuble-modal_type_location_id-type_location_choice_hidden',
        newInputId: 'update-immeuble-modal_type_location_id-new_type_location_input',
        formWrapper: 'update-immeuble-modal_type_location_id-new_type_location_wrapper',
        addButtonId: 'update-immeuble-modal_type_location_id-add_type_location_btn',
        ajaxUrl: '/add-choice/'
      },
      {
        listId: 'update-immeuble-modal_statut_batisse_id',
        hiddenId: 'update-immeuble-modal_statut_batisse_id-statut_choice_hidden',
        newInputId: 'update-immeuble-modal_statut_batisse_id-new_statut_input',
        formWrapper: 'update-immeuble-modal_statut_batisse_id-new_statut_wrapper',
        addButtonId: 'update-immeuble-modal_statut_batisse_id-add_statut_btn',
        ajaxUrl: '/add-choice/'
      },
      {
        listId: 'update-immeuble-modal_revetement_int_id',
        hiddenId: 'update-immeuble-modal_revetement_int_id-revetementinterieure_choice_hidden',
        newInputId: 'update-immeuble-modal_revetement_int_id-new_revetementinterieure_input',
        formWrapper: 'update-immeuble-modal_revetement_int_id-new_revetementinterieure_wrapper',
        addButtonId: 'update-immeuble-modal_revetement_int_id-add_revetementinterieure_btn',
        ajaxUrl: '/add-choice/'
      },
      {
        listId: 'update-immeuble-modal_revetement_ext_id',
        hiddenId: 'update-immeuble-modal_revetement_ext_id-revetementexterieure_choice_hidden',
        newInputId: 'update-immeuble-modal_revetement_ext_id-new_revetementexterieure_input',
        formWrapper: 'update-immeuble-modal_revetement_ext_id-new_revetementexterieure_wrapper',
        addButtonId: 'update-immeuble-modal_revetement_ext_id-add_revetementexterieure_btn',
        ajaxUrl: '/add-choice/'
      }
    ];
    dynamic_choices_list_objects.forEach(obj => {
      initDynamicChoiceList(obj.listId, obj.hiddenId, obj.newInputId, obj.formWrapper, obj.addButtonId, obj.ajaxUrl);
    });
    // add immeuble element dynamically
    const add_to_list_object = [
      {
        list_container: '#popup-elements-immeuble-container',
        list_input: 'popup-elements-immeuble-container-element-immeuble-input',
        list_btn: 'popup-elements-immeuble-container-add-element-btn',
        list_url: '/element-description-partial-form/'
      }
    ];
    add_to_list_object.forEach(obj => {
      FormUtils.addElementToList(obj.list_container, obj.list_input, obj.list_btn, obj.list_url);
    });
  },

  onClose: async $modal => {
    await FormPopulator.reloadElements('#main-elements-immeuble-container');
    await FormPopulator.reloadDynamicChoices({
      model: 'TypeConstructions',
      list_id: 'main_type_construction_id',
      checkbox_name: 'construction_choice_checkbox',
      hidden_name: 'construction_choice',
      hidden_id: 'main_type_construction_id-construction_choice_hidden',
      add_wrapper_id: 'main_type_construction_id-new_construction_wrapper',
      new_input_id: 'main_type_construction_id-new_construction_input',
      add_btn_id: 'main_type_construction_id-add_construction_btn'
    });
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
