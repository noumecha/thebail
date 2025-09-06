$(function () {
    // initialize modals for elementdescription
    loadModal('#create-elementdescription-modal', '#elementdescription-form-container', '/elementdescription/elementdescriptions/') // for create or update
    submitForm('#elementdescription-form', '/elementdescription/elementdescriptions/', '/elementdescription/elementdescriptions/all/') // save to db
    fetchDatas('/elementdescription/elementdescriptions/all/', '#elementdescription-search-form', '#elementdescription-table-container') // initial fetching
    filteringDatas('#search', '/elementdescription/elementdescriptions/all/', '#elementdescription-search-form', '#elementdescription-table-container') // filter elementdescriptions dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // show sucess messge or error message 
    showMessage()

})