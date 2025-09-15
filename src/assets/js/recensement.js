$(function () {

    // initialize modals for recensement
    loadModal('#create-recensement-modal', '#recensement-form-content', '/immeuble/recensements/') // for create or update
    submitForm('#recensementForm', '/immeuble/recensements/', '/immeuble/recensements/all/') // save to db
    fetchDatas('/immeuble/recensements/all/', '#recensement-search-form', '#recensement-table-container') // initial fetching
    filteringDatas('#search', '/immeuble/recensements/all/', '#recensement-search-form', '#recensement-table-container') // filter recensements dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
});
