// popup.js
$(function () {
  // Popup — à l'ouverture de la modale (pas au chargement !)
  $('#create-bailleur-modal').on('shown.bs.modal', function () {
    console.log('Modal ouverte, initialisation en cours...');
    // Initialiser Select2 pour les champs de la modale
    initSelect2Ajax($(this));
  });

  // Popup — à la fermeture de la modale, détruire les instances Select2 pour éviter les conflits à la réouverture
  $('#create-bailleur-modal').on('hidden.bs.modal', function () {
    $(this)
      .find('.select2-ajax')
      .each(function () {
        if ($(this).hasClass('select2-hidden-accessible')) {
          $(this).select2('destroy');
        }
      });
  });
});
