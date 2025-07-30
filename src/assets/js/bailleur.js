$(function () {
    loadModal('#create-bailleur-modal', '#bailleur-form-container', '/bailleur/bailleurs/')
    submitForm('#bailleur-form', '/bailleur/bailleurs/', '/bailleur/bailleurs/all/')
    fetchDatas('/bailleur/bailleurs/all/', '#bailleur-search-form', '#bailleur-table-container')
    filteringDatas('#search', '/bailleur/bailleurs/all/', '#bailleur-search-form', '#bailleur-table-container')
    clearSearch('#clearSearch', '#search')
    showMessage()
})