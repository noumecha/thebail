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

// form modal form inside another form
function ajaxModal(modalId, formnContainerId, formId, fetchUrl, selectItemId = null) {
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
                    $(selectContainer).append(
                        $('<option>', {
                            value: data.id,
                            text: data.text,
                            selected: true
                        })
                    );
                    $(formId).closest('form')[0].reset();
                    id = '#form-success-'+modalId.replace('#','')
                    showAlertMessage(data.message, id);
                } else {                        
                    id = '#form-error-'+modalId.replace('#','')
                    showAlertMessage(data.errors, id)
                }
            }
        });
    });
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
                    showAlertMessage(data.errors, '#form-error')
                }
            }
        });
    });
}

// set the success message after form submission is successful
function showAlertMessage(msg, id) {
    const msgBlock = $(id);
    msgBlock.stop(true, true).empty();

    if (typeof msg === 'object' && !Array.isArray(msg)) {
        // Handle JSON object with fields and arrays of messages
        const list = $('<ul></ul>');
        Object.keys(msg).forEach((key) => {
            msg[key].forEach((error) => {
                list.append($('<li></li>').text(`${key}: ${error}`));
            });
        });
        msgBlock.append(list);
    } else {
        // Handle string messages
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

// function to toogle visibility and required attribute of fields in form base on another field value
function setVisible(mainSelector, targetSelector = null, valueToShow = null) {
    // on change
    if (mainSelector) {
        $(document).on('change', mainSelector, function() {
            const selectedValue = $(this).val();
            //console.log("Selected value: ", selectedValue);
            if (selectedValue === valueToShow) {
                $(targetSelector).closest('.form-group').show();
                $(targetSelector).prop('required', true);
            } else {
                $(targetSelector).closest('.form-group').hide();
                $(targetSelector).prop('required', false);
                $(targetSelector).val('').trigger('change');
            }
        });
    } else {
        // hide all required field that are in a form-group that is hidden
        $('form').find(':input').each(function () {
            if (!$(this).is(':visible')) {
                $(this).prop('required', false);
            }
        });
    }
    
}

// toggle element visibility base on some slect element
/*function toogleFormset(selectElement, value = null, formsetToShow, formsetToHide) {
    if (selectElement) {
        $(document).on('change', selectElement, function() {
            const selectedValue = $(this).val();
            //console.log("Selected value: ", selectedValue);
            if (selectedValue === value) {
                $(formsetToShow).show();
                $(formsetToHide).hide();
            } else {
                $(formsetToShow).hide();
                $(formsetToHide).show();
            }
        });
    } else {
        $(formsetToShow).show();
        $(formsetToHide).show();
    }
}*/

function toogleFormset(selectElement, value = null, formsetToShow, formsetToHide) {
    if (selectElement) {
        $(document).on('change', selectElement, function() {
            const selectedValue = $(this).val();
            //console.log("Selected value: ", selectedValue);
            if (selectedValue === value) {
                $(formsetToShow).show();
                $(formsetToHide).hide();
            } else if (selectedValue === "1" || selectedValue === "2") {
                // If the value is the other specific value (1 or 2), hide the opposite formset
                $(formsetToShow).hide();
                $(formsetToHide).show();
            } else {
                // If the value is neither "1" nor "2", show both formsets
                $(formsetToShow).show();
                $(formsetToHide).show();
            }
        });

        // Trigger the change event on page load to handle initial state
        $(selectElement).trigger('change');
    } else {
        // If no selectElement is provided, show both formsets by default
        $(formsetToShow).show();
        $(formsetToHide).show();
    }
}