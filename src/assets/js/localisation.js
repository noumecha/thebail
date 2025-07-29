$(function () {
    // initialize modals for localisation
    loadModal('#create-localisation-modal', '#localisation-form-container', '/localisation/localisations/') // for create or update
    submitForm('#localisation-form', '/localisation/localisations/', '/localisation/localisations/all/') // save to db
    fetchDatas('/localisation/localisations/all/', '#localisation-search-form', '#localisation-table-container') // initial fetching
    filteringDatas('#searchFilter', '/localisation/localisations/all/', '#localisation-search-form', '#localisation-table-container') // filter localisations dynamically
    clearSearch('#clearSearch', '#searchFilter') // clear search input

    // show sucess messge or error message 
    showMessage()
})