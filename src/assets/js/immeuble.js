$(function () {
    // initialize modals for immeuble
    loadModal('#create-immeuble-modal', '#immeuble-form-container', '/immeuble/immeubles/') // for create or update
    submitForm('#immeuble-form', '/immeuble/immeubles/', '/immeuble/immeubles/all/') // save to db
    fetchDatas('/immeuble/immeubles/all/', '#immeuble-search-form', '#immeuble-table-container') // initial fetching
    filteringDatas('#search', '/immeuble/immeubles/all/', '#immeuble-search-form', '#immeuble-table-container') // filter immeubles dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})