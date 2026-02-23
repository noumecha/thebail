window.configs = window.configs || {};
window.configs.customMessages = {
  // Erreurs par champ spécifique
  'immeuble.type_construction_id': 'Veuillez sélectionner un type de construction',
  'immeuble.Date_Construction': "Veuillez définir la date de construction de l'immeuble",
  'immeuble.type_location_id': 'Veuillez sélectionner un type de location',
  'immeuble.statut_batisse_id': 'Veuillez sélectionner un statut de bâtisse',
  'immeuble.revetement_int_id': 'Veuillez sélectionner un type de revêtement intérieur',
  'immeuble.revetement_ext_id': 'Veuillez sélectionner un type de revêtement extérieur',
  'immeuble.Designation': 'Veuillez saisir la désignation du bien',
  'contrat.bailleur.Type_personne': 'Veuillez sélectionner le type de personne du bailleur',
  'contrat.Duree_Contrat': 'Veuillez saisir la durée du contrat'
};
window.configs.genericMessages = {
  'Un nombre entier valide est requis.': 'Veuillez sélectionner une option valide',
  'Ce champ est obligatoire.': 'Ce champ est requis',
  'This field is required.': 'Ce champ est requis',
  'A valid integer is required.': 'Veuillez sélectionner une option valide',
  'Enter a valid email address.': 'Veuillez saisir une adresse email valide'
};

/**
 * init select2 with ajax for a select element
 * @returns void
 */
function initSelect2Ajax($container = $(document), rowPrefix = null) {
  $container.find('.select2-ajax').each(function () {
    const $select = $(this);
    console.log('Initialisation de Select2 pour:', $select.attr('name'));
    // Éviter de réinitialiser si déjà initialisé
    if ($select.hasClass('select2-hidden-accessible')) {
      return;
    }

    const ajaxUrl = $select.data('ajax-url');
    const placeholder = $select.data('ajax-placeholder');
    const minLengthAttr = $select.attr('data-ajax-length');
    const minLength = minLengthAttr !== undefined && minLengthAttr !== '' ? parseInt(minLengthAttr) : 2;
    // 👇 Détection automatique du bon parent
    const $modalParent = $select.closest('.modal');
    const $dropdownParent = $modalParent.length ? $modalParent : $container;

    try {
      $select.select2({
        ajax: {
          url: ajaxUrl,
          dataType: 'json',
          delay: 250,
          data: function (params) {
            return { q: params.term || '', page: params.page || 1 };
          },
          processResults: function (data) {
            return {
              results: data.results,
              pagination: { more: data.pagination.more }
            };
          },
          cache: true
        },
        placeholder: placeholder || 'Rechercher...',
        minimumInputLength: minLength,
        dropdownParent: $dropdownParent,
        language: {
          inputTooShort: () => 'Veuillez saisir au moins 2 caractères',
          searching: () => 'Recherche en cours...',
          noResults: () => 'Aucun résultat trouvé'
        }
      });

      // ✅ Si minLength = 0, charger les résultats à l'ouverture (UNE SEULE FOIS)
      if (minLength === 0) {
        $select.on('select2:open', function () {
          // Charger les résultats seulement si le champ est vide
          if (!$(this).val()) {
            $(this).data('select2').trigger('query', { term: '' });
          }
        });
      }
    } catch (error) {
      console.error('Erreur Select2:', error);
    }
  });
}
