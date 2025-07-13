$(function () {

    // initialize modals
    loadModal('#create-recensement-modal', '#recensement-form-content', '/immeuble/recensements/form/');
    submitForm('#recensementForm', '/immeuble/recensements/form/')

    // function to set select2 on element of type select
    function setSelect2(selector, placeholder) {
        if($(selector).is('select')) {
            $(selector).select2({
                placeholder: placeholder,
                allowClear: true,
            });
        }
    }

    // function to load modal content
    function loadModal(modalId, formContainer, fetchUrl) {
        const formContent = $(formContainer);

        // Open modal and load form
        $(document).on('click', `[data-bs-target="${modalId}"]`, function () {
            $.get(fetchUrl, function (data) {
                formContent.html(data.html);
                //setSelect2('#id_Immeuble', 'Selectionnez un immeuble');
            });
        });
    }

    // function to handle form submission
    function submitForm(formId, fetchUrl) {
        $(document).on('submit', formId, function (e) {
            e.preventDefault();
            const form = $(this);
            const formData = form.serialize();

            // Send AJAX request
            $.ajax({
                url: fetchUrl,
                type: 'POST',
                data: formData,
                success: function (data) {
                    if (data.success) {
                        window.location.reload();
                        modal.hide();
                        showAlertMessage(data.message, '#form-success');
                    } else {
                        console.error("Error occurred : ", data);
                        showAlertMessage(data, '#form-error');
                    }
                }
            });
        });
    }

    // set the success message after form submission is successful
    function showAlertMessage(msg, id) {
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
});
