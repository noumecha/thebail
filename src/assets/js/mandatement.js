$(function () {
    // initialize modals for mandatement
    loadModal('#create-mandatement-modal', '#mandatement-form-container', '/mandatement/mandatements/') // for create or update
    submitForm('#mandatement-form', '/mandatement/mandatements/', '/mandatement/mandatements/all/') // save to db
    fetchDatas('/mandatement/mandatements/all/', '#mandatement-search-form', '#mandatement-table-container') // initial fetching
    filteringDatas('#search', '/mandatement/mandatements/all/', '#mandatement-search-form', '#mandatement-table-container') // filter mandatements dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})