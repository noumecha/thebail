/**
 * module de validation du formulaire
 */
export const Validators = {
  validatePiecesCollectees() {
    const errors = [];
    const $container = $('.pieces-collecte-container-tbody');

    $container.find('tr[data-piece-id]').each(function () {
      const $row = $(this);
      const elementId = $row.data('piece-id');
      const $checkbox = $row.find(`#piece_${elementId}`);
      const $numberInput = $row.find(`#piece_nombre_input_${elementId}`);
      const $imageInput = $row.find(`#piece_image_input_${elementId}`);
      const elementLabel = $row.find('label.form-check-label').text().trim();

      if ($checkbox.is(':checked')) {
        const quantity = parseInt($numberInput.val()) || 0;

        // ✅ Valider la quantité
        if (!quantity || quantity <= 0) {
          errors.push(`${elementLabel} : La quantité est obligatoire lorsque l'élément est coché`);
          return;
        }

        // ✅ Valider le nombre d'images
        const selectedFiles = $imageInput?.length || 0;
        const hasExistingImages = $row.find('.existing-image-item').length;
        const totalImages = selectedFiles + hasExistingImages;

        if (totalImages === 0) {
          errors.push(`${elementLabel} : Les images sont obligatoires lorsque l'élément est coché`);
        } else if (selectedFiles > quantity) {
          // ✅ Vérifier que le nombre d'images ne dépasse pas la quantité
          errors.push(
            `${elementLabel} : Vous avez sélectionné ${selectedFiles} images mais la quantité est ${quantity}`
          );
        }
      }
    });

    return errors;
  },

  validateElementsImmeuble() {
    const errors = [];
    const $container = $('#elements-immeuble-container');

    $container.find('tr[data-el-id]').each(function () {
      const $row = $(this);
      const elementId = $row.data('el-id');
      const $ouiCheckbox = $row.find(`#element_${elementId}_oui`);
      const $numberInput = $row.find(`#nombre_input_${elementId}`);
      const elementLabel = $row.find('label.text-capitalize').text().trim();

      if ($ouiCheckbox.is(':checked')) {
        const quantity = $numberInput.val();
        if (!quantity || quantity.trim() === '' || parseInt(quantity) <= 0) {
          errors.push(`${elementLabel}: La quantité est obligatoire lorsque "Oui" est sélectionné`);
        }
      }
    });

    return errors;
  }
};
