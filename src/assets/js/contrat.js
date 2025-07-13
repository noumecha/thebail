$(function() {
    // display and undisplay field base on nature field value
    $(document).on('change', '#id_nature_contrat', function () {
        var nature_contrat = $(this).val();
        console.log('nature_contrat :', nature_contrat);
    });

    // get strucutre base on the adminstiration value
    $('#id_Administration_beneficiaire').select2({
        placeholder: "Selectionnez une administration",
        allowClear: true,
    });
    $('#id_Structure').select2({
        placeholder : "Selectionnez une structure",
        allowClear: true,
    })
    $(document).on('change', '#id_Administration_beneficiaire', function () {
        let adminId = $(this).val();
        $('#id_Structure').empty().trigger('change');
        if (adminId) {
            $.ajax({
                url: '/structures/',
                data: {
                    "administration_id" : adminId
                },
                success: function(data) {
                    $('#id_Structure').append('<option value="">Selectionnez une structure</option>');
                    data.forEach(function(item) {
                        let newOption = new Option(item.text, item.id, false, false);
                        $('#id_Structure').append(newOption);
                    });
                    $('#id_Structure').trigger('change');
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching structures:', error);
                }
            });
        }
    })

    // immeuble 
    initAjaxModal("#addImmeubleModal", "#immeuble-form-content", "#immeubleForm",  "/immeuble-partial-form/", "#id_Immeubles")
    // bailleur
    initAjaxModal("#addBailleurModal", "#bailleur-form-content", "#bailleurForm",  "/bailleur-partial-form/", "#id_Bailleur")

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

    // set the success message after form submission is successful
    function setMessage(msg, id) {
        const msgBlock = $(id);
        msgBlock.stop(true, true).empty();
        if (Array.isArray(msg)) {
            const list = $('<ul></ul>');
            msg.forEach((m) => list.append($('<li></li>').text(m.key + ': ' + m.value)));
            msgBlock.append(list);
        } else {
            msgBlock.append($('<p class="text-center mb-0"></p>').text(msg));
        }

        msgBlock.fadeIn().css('display', 'block');
        setTimeout(() => msgBlock.fadeOut(), 7000);
    }

})