$(function () {
    // initialize modals for piece
    loadModal('#create-piece-modal', '#piece-form-container', '/piece/pieces/') // for create or update
    submitForm('#piece-form', '/piece/pieces/', '/piece/pieces/all/') // save to db
    fetchDatas('/piece/pieces/all/', '#piece-search-form', '#piece-table-container') // initial fetching
    filteringDatas('#search', '/piece/pieces/all/', '#piece-search-form', '#piece-table-container') // filter pieces dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()

})