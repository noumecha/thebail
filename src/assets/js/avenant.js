$(function () {
    // initialize modals for avenant
    loadModal('#create-avenant-modal', '#avenant-form-container', '/avenant/avenants/') // for create or update
    submitForm('#avenant-form', '/avenant/avenants/', '/avenant/avenants/all/') // save to db
    fetchDatas('/avenant/avenants/all/', '#avenant-search-form', '#avenant-table-container') // initial fetching
    filteringDatas('#searchFilter', '/avenant/avenants/all/', '#avenant-search-form', '#avenant-table-container') // filter avenants dynamically
    clearSearch('#clearSearch', '#searchFilter') // clear search input

    // show sucess messge or error message 
    showMessage()
})