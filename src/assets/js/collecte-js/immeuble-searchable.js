import { SearchableManager } from './modules/searchable-manager.js';
import { FormPopulator } from './modules/form-populator.js';
import { APIUtils } from './modules/api-utils.js';
new SearchableManager({
  listId: 'main_Designation',
  apiUrl: '/api/get-immeubles/',
  placeholder: 'Rechercher un immeuble ou ajouter un nouveau en saisissant sa Designation',
  getData: async id => {
    const response = await fetch(`/api/get-immeubles/${id}/`);
    const data = await response.json();
    return data;
  },
  onSelect: result => {
    $('#Designation-error').text('').toggleClass('d-none');
    FormPopulator.clearImmeubleForm();
  },
  populateFunction: data => {
    FormPopulator.populateImmeubleDatas(data.datas);
    if (data.datas.arrondissement_id) {
      APIUtils.generateFicheCollecte(data.datas.arrondissement_id);
    }
    if (data.is_linked_to_fiche) {
      $('#Designation-error').text('Cet immeuble est déjà lié à une fiche de collecte.').toggleClass('d-none');
    } else {
      $('#Designation-error').text('');
    }
  }
});
