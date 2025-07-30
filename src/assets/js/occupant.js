$(function () {
    // initialize modals for occupant
    loadModal('#create-occupant-modal', '#occupant-form-container', '/occupant/occupants/') // for create or update
    submitForm('#occupant-form', '/occupant/occupants/', '/occupant/occupants/all/') // save to db
    fetchDatas('/occupant/occupants/all/', '#occupant-search-form', '#occupant-table-container') // initial fetching
    filteringDatas('#search', '/occupant/occupants/all/', '#occupant-search-form', '#occupant-table-container') // filter occupants dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()
})