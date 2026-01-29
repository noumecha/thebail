$(function () {
  // setting all select option field to select2
  select2_elements_array = [
    '#matricule_responsable_collecte',
    '#pays_list,#region_list',
    '#departement_list',
    '#arrondissement_list',
    '#occupant_administration_list',
    '#structure_list',
    '#occupant_burreau_administration_list',
    '#avenant_1_ancien_bailleurs_list',
    '#avenant_1_nouveau_bailleurs_list',
    '#avenant_2_ancien_bailleurs_list',
    '#avenant_2_nouveau_bailleurs_list'
  ];
  select2_elements_array.forEach(function (element) {
    $(element).select2({
      allowClear: true
    });
  });

  // Quand l'administration change
  // structure_list administration_list
  $(document).on('change', '#administration_list', function () {
    var adminId = $(this).val();
    var serviceField = $('#ficheCollecteForm').find('#structure_list');
    var baseUrl = serviceField.data('autocomplete-light-url').split('?')[0];
    var newUrl = baseUrl + '?administration_id=' + adminId;
    serviceField.attr('data-autocomplete-light-url', newUrl);
    serviceField.val(null).trigger('change');
  });

  // select arrondissement and set other localisation informations automatically
  let region = $('#id_immeubles-0-region');
  let dpt = $('#id_immeubles-0-departement');
  let numero_collecte = $('#id_Numero_fiche_de_collecte');

  region.prop('readonly', true);
  dpt.prop('readonly', true);
  numero_collecte.prop('readonly', true);
  disabledCSS(region);
  disabledCSS(dpt);
  disabledCSS(numero_collecte);

  $(document).on('change', '#id_immeubles-0-arrondissement', function () {
    let arrondissement_id = $(this).val();
    $.ajax({
      url: '/arrondissement/',
      data: {
        arrondissement_id: arrondissement_id
      },
      success: function (data) {
        if (data.success) {
          region.val(data.region_id);
          dpt.val(data.dpt_id);
          numero_collecte.val(data.numero_collecte);
        } else {
          console.log('Aucune donnée trouvée ...');
        }
      },
      error: function (xhr, status, error) {
        console.error('Error getting data :', error);
      }
    });
  });

  /****  for inside form modal ***/
  // typecontrat
  ajaxModal(
    '#addTypeContratModal',
    '#typecontrat-form-content',
    '#typecontratForm',
    '/type-contrat-partial-form/',
    '#id_TypeContrat'
  );
  // revetementint-partial-form/, revetementext-partial-form/
  ajaxModal(
    '#addRevetementInterieureModal',
    '#revetementint-form-content',
    '#revetementintForm',
    '/revetement-int-partial-form/',
    '#id_immeubles-0-Revetement_interieure'
  );
  ajaxModal(
    '#addRevetementExterieureModal',
    '#revetementext-form-content',
    '#revetementextForm',
    '/revetement-ext-partial-form/',
    '#id_immeubles-0-Revetement_exterieure'
  );
  ajaxModal(
    '#addExerciceModal',
    '#exercice-form-content',
    '#exerciceForm',
    '/exercice-partial-form/',
    '#id_non_mandatements-0-Exercice'
  );
  ajaxModal('#addBailleurModal', '#bailleur-form-content', '#bailleurForm', '/bailleur-partial-form/', '#id_Bailleur');

  // element and pieces dynamic add with modal
  ajaxModal(
    '#addPieceModal',
    '#piece-form-content',
    '#pieceForm',
    '/piece-collecte-partial-form/',
    '#pieces-collecte-container'
  );

  // elements and pieces adding
  addElementToList(
    '#pieces-collecte-container',
    'piece-collecte-input',
    'add-piece-btn',
    '/piece-collecte-partial-form/'
  );
  addElementToList(
    '#elements-collecte-container',
    'element-immeuble-input',
    'add-element-btn',
    '/element-description-partial-form/'
  );
});
