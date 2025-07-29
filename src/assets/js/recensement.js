$(function () {

    // initialize modals for recensement
    loadModal('#create-recensement-modal', '#recensement-form-content', '/immeuble/recensements/') // for create or update
    submitForm('#recensementForm', '/immeuble/recensements/', '/immeuble/recensements/all/') // save to db
    fetchDatas('/immeuble/recensements/all/', '#recensement-search-form', '#recensement-table-container') // initial fetching
    filteringDatas('#searchFilter', '/immeuble/recensements/all/', '#recensement-search-form', '#recensement-table-container') // filter recensements dynamically
    clearSearch('#clearSearch', '#searchFilter') // clear search input

    // show sucess messge or error message 
    showMessage()
});
