$(function () {
  // initialize modals for periodiciterel
  loadModal('#create-periodiciterel-modal', '#periodiciterel-form-container', '/periodiciterel/periodiciterels/'); // for create or update
  submitForm('#periodiciterel-form', '/periodiciterel/periodiciterels/', '/periodiciterel/periodiciterels/all/'); // save to db
  fetchDatas('/periodiciterel/periodiciterels/all/', '#periodiciterel-search-form', '#periodiciterel-table-container'); // initial fetching
  filteringDatas(
    '#search',
    '/periodiciterel/periodiciterels/all/',
    '#periodiciterel-search-form',
    '#periodiciterel-table-container'
  ); // filter periodiciterels dynamically
  clearSearch('#clearSearch', '#search'); // clear search input

  // show sucess message or error message
  showMessage();
});
