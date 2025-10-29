$(function () {
  initCRUD({
    moduleName: 'utilisateur',
    baseUrl: '/utilisateur/utilisateurs/',
    fetchUrl: '/utilisateur/utilisateurs/all/',
    formSelector: '#utilisateurForm',
    modalSelector: '#create-utilisateur-modal',
    formContainerSelector: '#utilisateur-form-content',
    tableContainerSelector: '#utilisateur-table-container',
    searchFormSelector: '#utilisateur-search-form',
    searchInputSelector: '#search,#id_role,#id_cellule',
    clearBtnSelector: '#clearSearch'
  });
});
