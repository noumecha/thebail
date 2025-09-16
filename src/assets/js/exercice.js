$(function () {
    // initialize modals for exercice
    loadModal('#create-exercice-modal', '#exercice-form-container', '/exercice/exercices/') // for create or update
    submitForm('#exercice-form', '/exercice/exercices/', '/exercice/exercices/all/') // save to db
    fetchDatas('/exercice/exercices/all/', '#exercice-search-form', '#exercice-table-container') // initial fetching
    filteringDatas('#search', '/exercice/exercices/all/', '#exercice-search-form', '#exercice-table-container') // filter exercices dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})