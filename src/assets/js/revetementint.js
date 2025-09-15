$(function () {
    // initialize modals for revetementint
    loadModal('#create-revetementint-modal', '#revetementint-form-container', '/revetementint/revetementints/') // for create or update
    submitForm('#revetementint-form', '/revetementint/revetementints/', '/revetementint/revetementints/all/') // save to db
    fetchDatas('/revetementint/revetementints/all/', '#revetementint-search-form', '#revetementint-table-container') // initial fetching
    filteringDatas('#search', '/revetementint/revetementints/all/', '#revetementint-search-form', '#revetementint-table-container') // filter revetementints dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})