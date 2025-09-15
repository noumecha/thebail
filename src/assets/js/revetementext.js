$(function () {
    // initialize modals for revetementext
    loadModal('#create-revetementext-modal', '#revetementext-form-container', '/revetementext/revetementexts/') // for create or update
    submitForm('#revetementext-form', '/revetementext/revetementexts/', '/revetementext/revetementexts/all/') // save to db
    fetchDatas('/revetementext/revetementexts/all/', '#revetementext-search-form', '#revetementext-table-container') // initial fetching
    filteringDatas('#search', '/revetementext/revetementexts/all/', '#revetementext-search-form', '#revetementext-table-container') // filter revetementexts dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})