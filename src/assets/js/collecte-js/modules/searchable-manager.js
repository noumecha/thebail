import { FormUtils } from './form-utils.js';
export class SearchableManager {
  constructor(config) {
    this.listId = config.listId;
    this.apiUrl = config.apiUrl;
    this.placeholder = config.placeholder || 'Rechercher...';
    this.onSelect = config.onSelect || null;
    this.minLength = config.minLength || 2;
    this.populateFunction = config.populateFunction || null;
    this.getData = config.getData || null;

    this.init();
  }

  init() {
    // init the select2 with tags and ajax
    $(`#${this.listId}`).select2({
      ajax: {
        url: this.apiUrl,
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return { q: params.term || '', page: params.page || 1 };
        },
        processResults: function (data) {
          return {
            results: data.results,
            pagination: { more: data.pagination.more }
          };
        },
        error: () => {
          console.error('Erreur lors du chargement des options');
          return { results: [] };
        },
        cache: true
      },
      placeholder: this.placeholder,
      minimumInputLength: this.minLength,
      language: {
        inputTooShort: () => 'Veuillez saisir au moins 2 caractères',
        searching: () => 'Recherche en cours...',
        noResults: () => 'Aucun résultat trouvé'
      },
      tags: true,
      width: '100%'
    });
    // handle select event
    $(`#${this.listId}`).on('select2:select', async e => {
      const result = e.params.data;
      this.onSelect && this.onSelect(result);
      if (result?.id !== result?.text) {
        const data = await this.getData(result.id);
        this.populateFunction && this.populateFunction(data);
      }
    });
  }
}
