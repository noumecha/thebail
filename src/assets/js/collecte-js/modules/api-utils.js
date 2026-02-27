/**
 * module for API calls
 */
export const APIUtils = {
  // ✅ Générer le numéro de fiche de collecte
  async generateFicheCollecte(arrondissementId) {
    const params = new URLSearchParams({
      arrondissement_id: arrondissementId,
      ...(this.isEditMode && { edit_mode: 'true', fiche_id: this.ficheId })
    });
    let url = `/api/fiches/numero/?${params.toString()}`;
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        }
      });
      const result = await response.json();
      if (response.ok && result.success) {
        const numeroField = document.getElementById('Numero_fiche_de_collecte');
        if (numeroField) {
          numeroField.value = result.numero_collecte;
          showNotification('Numéro de fiche généré automatiquement', 'success');
        }
        // also set automatically region an departement values
        const region_select = $('#region');
        const departement_select = $('#departement');

        let regionId = result.region_id;
        let departementId = result.dpt_id;
        let region_libelle = result.region;
        let departement_libelle = result.departement;

        region_select.val(regionId).trigger('change');
        departement_select.val(departementId).trigger('change');

        let $region_option = region_select.find('option[value="' + regionId + '"]');
        let $departement_option = departement_select.find('option[value="' + departementId + '"]');

        if ($region_option.length) {
          $region_option.text(region_libelle);
        } else {
          region_select.append(new Option(region_libelle, regionId, true, true));
          region_select.trigger('change');
        }

        if ($departement_option.length) {
          $departement_option.text(departement_libelle);
        } else {
          departement_select.append(new Option(departement_libelle, departementId, true, true));
          departement_select.trigger('change');
        }
      } else {
        console.error('Erreur génération numéro:', result.error);
        showNotification(result.error || 'Erreur lors de la génération du numéro', 'warning');
      }
    } catch (error) {
      console.error('❌ Erreur génération numéro:', error);
      showNotification('Erreur lors de la génération du numéro de fiche', 'danger');
    }
  }
};
