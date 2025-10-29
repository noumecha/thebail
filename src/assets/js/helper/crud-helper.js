/**
 * Initialize CRUD module dynamically
 * @param {Object} config
 */
function initCRUD(config) {
  const {
    moduleName, // e.g. "cellule"
    baseUrl, // e.g. "/cellule/cellules/"
    fetchUrl, // e.g. "/cellule/cellules/all/"
    formSelector, // e.g. "#celluleForm"
    modalSelector, // e.g. "#create-cellule-modal"
    formContainerSelector, // e.g. "#cellule-form-content"
    tableContainerSelector, // e.g. "#cellule-table-container"
    searchFormSelector, // e.g. "#cellule-search-form"
    searchInputSelector, // e.g. "#search"
    clearBtnSelector // e.g. "#clearSearch"
  } = config;
  // Initialize modal for create/update
  loadModal(modalSelector, formContainerSelector, baseUrl);
  // Submit form (create/update)
  submitForm(formSelector, baseUrl, fetchUrl);
  // Fetch initial data
  fetchDatas(fetchUrl, searchFormSelector, tableContainerSelector);
  filteringDatas(searchInputSelector, fetchUrl, searchFormSelector, tableContainerSelector); // automatic refresh when change filter
  // Clear search field
  clearSearch(clearBtnSelector, searchInputSelector);
  // refresh
  refresh('#refresh-button', fetchUrl, searchFormSelector, tableContainerSelector);
  // Show success/error messages
  showMessage();
}
// Expose globally (so you can call it in any module JS)
window.initCRUD = initCRUD;
