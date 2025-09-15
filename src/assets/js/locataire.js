$(function () {
    loadModal('#create-locataire-modal', '#locataire-form-container', '/locataire/locataires/')
    submitForm('#locataire-form', '/locataire/locataires/', '/locataire/locataires/all/')
    fetchDatas('/locataire/locataires/all/', '#locataire-search-form', '#locataire-table-container')
    filteringDatas('#search', '/locataire/locataires/all/', '#locataire-search-form', '#locataire-table-container')
    clearSearch('#clearSearch', '#search')
    showMessage()
})