import { SearchableManager } from './modules/searchable-manager.js';
import { FormPopulator } from './modules/form-populator.js';
import { APIUtils } from './modules/api-utils.js';
new SearchableManager({
  listId: 'Designation',
  apiUrl: '/api/get-immeubles/',
  placeholder: 'Rechercher un immeuble ou ajouter un nouveau en saisissant sa Designation',
  getData: async id => {
    const response = await fetch(`/api/get-immeubles/${id}/`);
    const data = await response.json();
    return data;
  },
  populateFunction: data => {
    console.log('data', data.datas);
    FormPopulator.populateImmeubleDatas(data.datas);
    console.log('arrondissement_id : ', data.datas.arrondissement_id || 0);
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
