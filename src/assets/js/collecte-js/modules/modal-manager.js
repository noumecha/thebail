import { FormUtils } from './form-utils.js';
export class ModalManager {
  constructor(config) {
    this.modalId = config.modalId;
    this.mainListId = config.mainListId;
    this.formId = config.formId;
    this.onSuccess = config.onSuccess || null;
    this.onOpen = config.onOpen || null;
    this.onClose = config.onClose || null;
    this.collectFormData = config.collectFormData || this.collectFormData;

    this.init();
  }

  init() {
    const $modal = $(this.modalId);

    $modal.on('shown.bs.modal', event => {
      if (this.onOpen) this.onOpen($modal);
      const button = $(event.relatedTarget);
      const mainList = button.data('main-list');
      this.currentMainListId = mainList ? '#' + mainList : this.mainListId;
    });

    $modal.on('hidden.bs.modal', () => {
      if (this.onClose) this.onClose($modal);
    });

    $(document).on('submit', this.formId, e => {
      e.preventDefault();
      this.submitForm(e.target);
    });
  }

  async collectFormData() {
    const formData = new FormData($(this.formId)[0]);
    return formData;
  }

  async submitForm(form) {
    try {
      FormUtils.showLoader(form);
      const data = await this.collectFormData();
      console.log('data : ', data);
      const response = await fetch(form.action, {
        method: 'POST',
        body: JSON.stringify(data),
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application/json',
          'X-CSRFToken': FormUtils.getCSRFToken()
        }
      });
      const result = await response.json();
      console.log('📥 Réponse serveur:', result);
      if (response.ok && result.success) {
        if (this.onSuccess) this.onSuccess(result, this.currentMainListId);
      } else {
        FormUtils.showErrors([result.message || 'Erreur lors de la soumission'], form);
        FormUtils.handleServerErrors(result, form);
        console.error('Erreurs de validation:', result.errors);
      }
    } catch (error) {
      console.error('Erreur:', error);
      FormUtils.showErrors(['Une erreur est survenue lors de la soumission'], form);
    } finally {
      FormUtils.hideLoader(form);
    }
  }
}
