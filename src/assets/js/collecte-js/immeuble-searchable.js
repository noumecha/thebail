import { SearchableManager } from './modules/searchable-manager.js';
import { FormPopulator } from './modules/form-populator.js';
import { FormUtils } from './modules/form-utils.js';
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
  onSelect: result => {
    $('#Designation-error').text('').toggleClass('d-none');
    // re-init the form populated
    FormUtils.initElementsImmeuble();
    FormPopulator.clearDynamicChoice('type_construction_id');
    FormPopulator.clearDynamicChoice('type_location_id');
    FormPopulator.clearDynamicChoice('statut_batisse_id');
    FormPopulator.clearDynamicChoice('revetement_int_id');
    FormPopulator.clearDynamicChoice('revetement_ext_id');
    FormPopulator.clearOccupants('logementsManager');
    FormPopulator.clearOccupants('bureauxManager');
    FormPopulator.clearValue('Designation');
    FormPopulator.clearValue('Date_Construction');
    FormPopulator.clearValue('Nombre_de_pieces');
    FormPopulator.clearValue('Superficie_louer');
    FormPopulator.clearValue('observation');
    FormPopulator.clearValue('Quartier');
    FormPopulator.clearValue('Coordonee_gps');
    FormPopulator.clearValue('Ville');
    FormPopulator.clearValue('Rue');
    FormPopulator.clearSelect2Value('pays');
    FormPopulator.clearSelect2Value('region');
    FormPopulator.clearSelect2Value('departement');
    FormPopulator.clearSelect2Value('arrondissement');
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
