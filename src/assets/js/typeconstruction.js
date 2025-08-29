$(function () {
    // initialize modals for typeconstruction
    loadModal('#create-typeconstruction-modal', '#typeconstruction-form-container', '/typeconstruction/typeconstructions/') // for create or update
    submitForm('#typeconstruction-form', '/typeconstruction/typeconstructions/', '/typeconstruction/typeconstructions/all/') // save to db
    fetchDatas('/typeconstruction/typeconstructions/all/', '#typeconstruction-search-form', '#typeconstruction-table-container') // initial fetching
    filteringDatas('#search', '/typeconstruction/typeconstructions/all/', '#typeconstruction-search-form', '#typeconstruction-table-container') // filter typeconstructions dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})