$(function () {
    // initialize modals for avenant
    loadModal('#create-avenant-modal', '#avenant-form-container', '/avenant/avenants/') // for create or update
    submitForm('#avenant-form', '/avenant/avenants/', '/avenant/avenants/all/') // save to db
    fetchDatas('/avenant/avenants/all/', '#avenant-search-form', '#avenant-table-container') // initial fetching
    filteringDatas('#search', '/avenant/avenants/all/', '#avenant-search-form', '#avenant-table-container') // filter avenants dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})