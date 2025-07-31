$(function () {
    // initialize modals for non_mandatement
    loadModal('#create-non_mandatement-modal', '#non_mandatement-form-container', '/non_mandatement/non_mandatements/') // for create or update
    submitForm('#non_mandatement-form', '/non_mandatement/non_mandatements/', '/non_mandatement/non_mandatements/all/') // save to db
    fetchDatas('/non_mandatement/non_mandatements/all/', '#non_mandatement-search-form', '#non_mandatement-table-container') // initial fetching
    filteringDatas('#search', '/non_mandatement/non_mandatements/all/', '#non_mandatement-search-form', '#non_mandatement-table-container') // filter non_mandatements dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})