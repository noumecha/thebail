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
        btn = $('#save-btn')
        updateId = $('#update-id')
        btn.removeClass('btn-outline-primary btn-outline-success');
        if (action === "update") {
            url = url + "edit/" + id
            updateId.val(id)
            btn.text('Mettre à jour')
            btn.addClass('btn-outline-success btn-outline-success')
        } else {
            url = url + "form" 
            btn.text("Enregistrer")
            btn.addClass('btn-outline-primary btn-outline-primary')
        }
        $.get(url, function (data) {
            formContent.html(data.html);    
            setSelect2('#id_Immeuble', 'Selectionnez un immeuble', modalId);
        });
        url = ""
    });
}

// clearing search form 
function clearSearch(clearButton, searchInput) {    
    $(clearButton).on('click', function() {
        $(searchInput).val('').trigger('change');
    });
}

// function for filter actualites dynamically with filters
function filteringDatas(filters, url, formId, containerId) {
    $(filters).on('change keyup', function (e) {
        e.preventDefault();
        // clear any previous timeout
        clearTimeout($(this).data('timer'));
        $(this).data('timer', setTimeout(fetchDatas(url, formId, containerId), 500));
    });
}

// function to fecth datas
function fetchDatas(url, formId = null, containerId) {
    var formData = formId ? $(formId).serialize() : '';
    $.ajax({
        url: url,
        data: formData,
        type: 'GET',
        success: function (data) {
            if (data.success) {
                $(containerId).html(data.html);
            } else {
                console.error("Error occurred while fetching data : ", data.message);
            }
        },
    })
}

// function to handle form submission
function submitForm(formId, url, fetchUrl) {
    $(document).on('submit', formId, function (e) {
        e.preventDefault();
        const form = $(this);
        const formData = form.serialize();
        const saveUrl = $('#save-btn').text() === 'Mettre à jour' ? url + "update/" : url
        const updateId = $('#update-id').val();
        // console.log("Submitting form to: ", saveUrl + (updateId ? updateId : ''));
        // Send AJAX request
        $.ajax({
            url: saveUrl + (updateId ? updateId : ''),
            type: 'POST',
            data: formData,
            success: function (data) {
                if (data.success) {
                    showAlertMessage(data.message, '#form-success')
                    form.closest('form')[0].reset()
                    // on need to add something for proper refresh ps: containerId is the table container
                    fetchDatas(fetchUrl)
                } else {
                    console.error("Error occurred on submit : ", data.message)
                    showAlertMessage(data.message, '#form-error')
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