$(function() {
    // display and undisplay field base on nature field value
    $(document).on('change', '#id_nature_contrat', function () {
        var nature_contrat = $(this).val();
        console.log('nature_contrat :', nature_contrat);
    });

    // immeuble 
    initAjaxModal("#addImmeubleModal", "#immeuble-form-content", "#immeubleForm",  "/immeuble-form/", "#id_Immeubles")
    // bailleur
    initAjaxModal("#addBailleurModal", "#bailleur-form-content", "#bailleurForm",  "/bailleur-form/", "#id_Bailleur")

    // modularize code : 
    function initAjaxModal(modalId, formnContainerId, formId, fetchUrl, selectItemId = null) {
        const modal = new bootstrap.Modal($(modalId)[0]);
        const formContainer = $(formnContainerId);
        const selectContainer = $(selectItemId);

        // Ouvrir le modal et charger le formulaire
        $(document).on('click', '[data-bs-target="'+modalId+'"]', function () {
            $.get(fetchUrl, function (data) {
                formContainer.html(data.html);
            });
        });

        // Gérer la soumission AJAX du formulaire
        $(document).on('submit', `${formId}`, function (e) {
            e.preventDefault();

            const form = $(this);
            const formData = form.serialize();

            // delete mask field that'are required but not visible
            $(form).find(':input').each(function () {
                if (!$(this).is(':visible')) {
                    $(this).prop('required', false);
                }
            });

            // send ajax request
            $.ajax({
                url: fetchUrl,
                type: 'POST',
                data: formData,
                success: function (data) {
                    if (data.success) {
                        selectContainer.append(
                            $('<option>', {
                                value: data.id,
                                text: data.text,
                                selected: true
                            })
                        );
                        modal.hide();
                    } else {
                        formContainer.html(data.html);
                    }
                }
            });
        });
    }

})