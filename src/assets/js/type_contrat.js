$(function () {
    // initialize modals for typecontrat
    loadModal('#create-typecontrat-modal', '#typecontrat-form-container', '/typecontrat/typecontrats/') // for create or update
    submitForm('#typecontrat-form', '/typecontrat/typecontrats/', '/typecontrat/typecontrats/all/') // save to db
    fetchDatas('/typecontrat/typecontrats/all/', '#typecontrat-search-form', '#typecontrat-table-container') // initial fetching
    filteringDatas('#search', '/typecontrat/typecontrats/all/', '#typecontrat-search-form', '#typecontrat-table-container') // filter typecontrats dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})