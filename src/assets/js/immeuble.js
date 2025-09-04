$(function () {
    // initialize modals for immeuble
    loadModal('#create-immeuble-modal', '#immeuble-form-container', '/immeuble/immeubles/') // for create or update
    submitForm('#immeuble-form', '/immeuble/immeubles/', '/immeuble/immeubles/all/') // save to db
    fetchDatas('/immeuble/immeubles/all/', '#immeuble-search-form', '#immeuble-table-container') // initial fetching
    filteringDatas('#search', '/immeuble/immeubles/all/', '#immeuble-search-form', '#immeuble-table-container') // filter immeubles dynamically
    clearSearch('#clearSearch', '#search') // clear search input

    // construction
    initAjaxModal("#addConstructionModal", "#construction-form-content", "#constructionForm",  "/construction-partial-form/", "#id_Construction")

    // modularize code : 
    function initAjaxModal(modalId, formnContainerId, formId, fetchUrl, selectItemId = null) {
        const modal = $(modalId);
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
                        setMessage(data.message, '#form-success');
                        modal.hide();
                        $('.modal-backdrop').remove(); // remove backdrop
                        formContainer.empty(); // clear the form content
                    } else {                        
                        errors = Array.from(Object.entries(data.errors), ([key, value]) => ({
                            key, value
                        }))
                        setMessage(errors, '#form-error');
                    }
                }
            });
        });
    }

    // show sucess messge or error message 
    showMessage()
})