/**
 * fichier dédié à la gestion des dépendances entre champs, notamment pour les champs de type checkbox
 * exemple : le champ Role_bailleur qui doit être désactivé tant que le champ Statut_bailleur n'est pas coché
 * @param {*} statutSelector : le sélecteur du champ statut (ex: '#create-bailleur-modal_Statut_bailleur')
 * @param {*} roleSelector : le sélecteur du champ rôle (ex: '#create-bailleur-modal_Role_bailleur')
 * @return void
 */
export function bindStatutRoleDependency(statutSelector, roleSelector) {
  // 🔥 On retire les anciens handlers avant d'en ajouter
  $(statutSelector).off('change.dependency');

  const isStatutChecked = $(`${statutSelector} .dynamic-check`).is(':checked');
  $(`${roleSelector} .dynamic-check`).prop('disabled', !isStatutChecked);

  $(statutSelector).on('change.dependency', '.dynamic-check', function () {
    const isChecked = $(this).is(':checked');

    $(`${roleSelector} .dynamic-check`).prop('disabled', !isChecked);

    if (!isChecked) {
      $(`${roleSelector} .dynamic-check`).prop('checked', false).trigger('change');
    }
  });
}
