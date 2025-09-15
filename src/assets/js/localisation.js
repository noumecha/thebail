$(function () {
    // initialize modals for localisation
    loadModal('#create-localisation-modal', '#localisation-form-container', '/localisation/localisations/') // for create or update
    submitForm('#localisation-form', '/localisation/localisations/', '/localisation/localisations/all/') // save to db
    fetchDatas('/localisation/localisations/all/', '#localisation-search-form', '#localisation-table-container') // initial fetching
    filteringDatas('#search', '/localisation/localisations/all/', '#localisation-search-form', '#localisation-table-container') // filter localisations dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()

    // set visibility on modal load initialization
    $('#create-localisation-modal').on('shown.bs.modal', function () {
        setVisible('#id_Type_localisation', '#id_Ville, #id_Rue', '1') // 1 - Extérieure
        setVisible('#id_Type_localisation', '#id_region, #id_departement, #id_arrondissement, #id_Quartier', '2') // 2 - National
    });

})