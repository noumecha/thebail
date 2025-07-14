$(function () {

    // initialize modals for recensement
    loadModal('#create-recensement-modal', '#recensement-form-content', '/immeuble/recensements/') // for create or update
    submitForm('#recensementForm', '/immeuble/recensements/', '#recensement-table') // save to db
    
    // show sucess messge or error message 
    showMessage()

    // function to set select2 on element of type select
    function setSelect2(selector, placeholder, modalId) {
        if($(selector).is('select')) {
            $(selector).select2({
                placeholder: placeholder,
                allowClear: true,
                dropdownParent: $(modalId),
            });
        }
    }

    // function to load modal content
    function loadModal(modalId, formContainer, url) {
        const formContent = $(formContainer);
        // Open modal and load form
        $(document).on('click', `[data-bs-target="${modalId}"]`, function () {
            action = $(this).data('action')
            const id = $(this).data('id')
            url = action === "update" ? url + "update/" + id : url + "form" 
            $.get(url, function (data) {
                formContent.html(data.html);
                setSelect2('#id_Immeuble', 'Selectionnez un immeuble', modalId);
            });
            url = ""
        });
    }

    // function to fecth data
    function fetchDatas(url, containerId) {
        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                if (data.success) {
                    $(containerId).html(data.html);
                } else {
                    console.error("Error occurred while fetching data : ", data);
                }
            },
        })
    }

    // function to handle form submission
    function submitForm(formId, url, containerId) {
        $(document).on('submit', formId, function (e) {
            e.preventDefault();
            const form = $(this);
            const formData = form.serialize();

            // Send AJAX request
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                success: function (data) {
                    if (data.success) {
                        showAlertMessage(data.message, '#form-success')
                        form.closest('form')[0].reset()
                        fetchDatas(url, containerId)
                    } else {
                        console.error("Error occurred : ", data)
                        showAlertMessage(data, '#form-error')
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
        setTimeout(() => msgBlock.fadeOut(), 5000);
    }

    // show message 
    function showMessage() {
        container = $("#message-show")
        container.fadeIn().css('display', 'block');
        setTimeout(() => container.fadeOut(), 5000);
    }
});
