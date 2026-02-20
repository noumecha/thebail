// function to set select2 on element of type select
function setSelect2(selector, placeholder, modalId) {
  if ($(selector).is('select')) {
    $(selector).select2({
      placeholder: placeholder,
      allowClear: true,
      dropdownParent: $(modalId)
    });
  }
}

// set the success message after form submission is successful
function setMessage(msg, id) {
  const msgBlock = $(id);
  msgBlock.stop(true, true).empty();
  if (Array.isArray(msg)) {
    const list = $('<ul></ul>');
    msg.forEach(m => list.append($('<li></li>').text(m.key + ': ' + m.value)));
    msgBlock.append(list);
  } else {
    msgBlock.append($('<p class="text-center mb-0"></p>').text(msg));
  }
  msgBlock.fadeIn().css('display', 'block');
  setTimeout(() => msgBlock.fadeOut(), 7000);
}

// form modal form inside another form
function ajaxModal(modalId, formContainerId, formId, fetchUrl, selectItemId = null) {
  const modal = $(modalId);
  const formContainer = $(formContainerId);
  const selectContainer = $(selectItemId);

  $(document).on('click', '[data-bs-target="' + modalId + '"]', function () {
    $.get(fetchUrl, function (data) {
      formContainer.html(data.html);
    });
  });

  $(document).on('submit', `${formId}`, function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();

    $(form)
      .find(':input')
      .each(function () {
        if (!$(this).is(':visible')) $(this).prop('required', false);
      });

    $.ajax({
      url: fetchUrl,
      type: 'POST',
      data: formData,
      success: function (data) {
        if (data.success) {
          if (selectContainer && selectContainer.length && !data.html) {
            $(selectContainer).append($('<option>', { value: data.id, text: data.text, selected: true }));
          }
          if (data.html) {
            // append data to the last child of selectContainer
            //$(selectContainer).append(data.html);
            appendToDynamicGroup(selectContainer, data.html);
          }

          $(formId).closest('form')[0].reset();
          const id = '#form-success-' + modalId.replace('#', '');
          showAlertMessage(data.message, id);

          const modalInstance = bootstrap.Modal.getInstance(document.querySelector(modalId));
          modalInstance.hide();
        } else {
          const id = '#form-error-' + modalId.replace('#', '');
          showAlertMessage(data.errors, id);
        }
      }
    });
  });
}

// apppending dynamic group
const GROUP_HEADERS = {
  element: `
    <thead class="table-light">
      <tr>
        <th class="p-0">Existence</th>
        <th class="bg-secondary-subtle p-0"></th>
        <th class="p-0">Quantité</th>
      </tr>
    </thead>
  `,
  piece: `
    <thead class="table-light">
      <tr>
        <th class="p-0">Désignation</th>
        <th class="p-0">Quantité</th>
        <th class="p-0">Images</th>
      </tr>
    </thead>
  `
};

// form for element inside another form
function addElementToList(listId, newInputId, addBtnId, url) {
  const selectContainer = $(listId);
  $('#' + addBtnId).click(function () {
    const val = $('#' + newInputId)
      .val()
      .trim();
    if (!val) return;
    console.log('select container : ', selectContainer);
    console.log(`variables : listid = ${listId}
      newinputId = ${newInputId}; addBtnId = ${addBtnId}; url = ${url}; val = ${val}`);
    if (url) {
      $.post({
        url: url,
        data: {
          libelle: val,
          model: selectContainer.data('model')
        },
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      }).done(function (data) {
        console.log('data : ', data);
        if (data.html) {
          appendToDynamicGroup(listId, data.html);
        }
        if (data.success) {
          showAlertMessage(data.message, '#form-success');
        } else {
          showAlertMessage(data.errors, '#form-error');
        }
      });
    } else {
      console.log('error');
      showAlertMessage(data.message, '#form-error');
    }
    $('#' + newInputId).val('');
  });
}

function appendToDynamicGroup(containerSelector, newRowHtml) {
  const $container = $(containerSelector);
  console.log('container : ', $container);
  const groupType = $container.data('group-type');
  console.log('group type : ', groupType);
  const maxItems = parseInt($container.data('max-items')) || 9;

  // Find last group
  let $lastGroup = $container.find('.col-block').last();

  // If no group exists, create one
  if (!$lastGroup.length) {
    $lastGroup = createNewGroup($container, groupType);
    $container.append($lastGroup);
  }

  const $tbody = $lastGroup.find('tbody');
  const currentCount = $tbody.find('tr').length;

  // If last group is full, create a new one
  if (currentCount >= maxItems) {
    const $newGroup = createNewGroup($container, groupType);
    $container.append($newGroup);
    $newGroup.find('tbody').append(newRowHtml);
  } else {
    $tbody.append(newRowHtml);
  }
}

function createNewGroup($container, type) {
  const headerHtml = GROUP_HEADERS[type] || '';
  const colClass = type === 'piece' ? 'col-md-6 col-lg-4' : 'col-md-4';

  const $newGroup = $(`
    <div class="${colClass} col-block mb-4">
      <table class="table align-middle text-center">
        ${headerHtml}
        <tbody class="${type}-collecte-container-tbody"></tbody>
      </table>
    </div>
  `);

  return $newGroup;
}

// generic function to mange checkboxes in the dynamic groups
document.addEventListener('change', function (e) {
  if (e.target.classList.contains('statut-checkbox')) {
    const group = e.target.getAttribute('data-group');
    if (e.target.checked) {
      document.querySelectorAll(`.statut-checkbox[data-group='${group}']`).forEach(cb => {
        if (cb !== e.target) cb.checked = false;
      });
    }
  }
});

// function to load modal content
function loadModal(modalId, formContainer, url) {
  const formContent = $(formContainer);
  $(document).on('click', `[data-bs-target="${modalId}"]`, function (e) {
    e.preventDefault();
    action = $(this).data('action');
    const id = $(this).data('id');
    btn = $('#save-btn');
    updateId = $('#update-id');
    btn.removeClass('btn-outline-primary btn-outline-success');
    if (action === 'update') {
      url = url + 'edit/' + id;
      updateId.val(id);
      btn.text('Mettre à jour');
      btn.addClass('btn-outline-success btn-outline-success');
    } else {
      url = url + 'form';
      btn.text('Enregistrer');
      btn.addClass('btn-outline-primary btn-outline-primary');
    }
    $.get(url, function (data) {
      formContent.html(data.html);
    });
    url = '';
  });
}

// clearing search form
function clearSearch(clearButton, searchInput) {
  $(clearButton).on('click', function () {
    $(searchInput).val('').trigger('change');
  });
}

// function for filter actualites dynamically with filters
function filteringDatas(searchInputSelector, url, formId, containerId) {
  $(searchInputSelector).on('change keyup', function (e) {
    e.preventDefault();
    // clear any previous timeout
    clearTimeout($(this).data('timer'));
    $(this).data('timer', setTimeout(fetchDatas(url, formId, containerId), 500));
  });
}

// when refresh run fetchDatas function
function refresh(refreshBtn, url, formId, containerId) {
  $(refreshBtn).on('click', function () {
    fetchDatas(url, formId, containerId);
  });
}

function fetchDatas(url, formId = null, containerId) {
  const formData = formId ? $(formId).serialize() : '';
  const loader = $('#table-loader');
  const table_container = $('#data-table');
  loader.removeClass('d-none');
  table_container.hide();
  $.ajax({
    url: url,
    data: formData,
    type: 'GET',
    beforeSend: function () {
      loader.removeClass('d-none');
    },
    success: function (data) {
      if (data.success) {
        $(containerId).html(data.html);
      } else {
        console.error('Error occurred while fetching data : ', data.message);
      }
    },
    error: function (xhr, status, error) {
      console.error('AJAX Error:', error);
    },
    complete: function () {
      loader.addClass('d-none');
      table_container.show();
    }
  });
}

// function to handle form submission
function submitForm(formId, url, fetchUrl) {
  $(document).on('submit', formId, function (e) {
    e.preventDefault();
    const form = $(this);
    const formData = form.serialize();
    const saveUrl = $('#save-btn').text() === 'Mettre à jour' ? url + 'update/' : url;
    console.log(saveUrl);
    const updateId = $('#update-id').val();
    // Send AJAX request
    $.ajax({
      url: saveUrl + (updateId ? updateId : ''),
      type: 'POST',
      data: formData,
      success: function (data) {
        if (data.success) {
          showAlertMessage(data.message, '#form-success');
          form.closest('form')[0].reset();
        } else {
          console.error('Error occurred on submit : ', data.message);
          showAlertMessage(data.errors, '#form-error');
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
    Object.keys(msg).forEach(key => {
      msg[key].forEach(error => {
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
  container = $('#message-show');
  container.fadeIn().css('display', 'block');
  setTimeout(() => container.fadeOut(), 3000);
}

// function to toogle visibility and required attribute of fields in form base on another field value
function setVisible(mainSelector, targetSelector = null, valueToShow = null) {
  // on change
  if (mainSelector) {
    $(document).on('change', mainSelector, function () {
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
    $('form')
      .find(':input')
      .each(function () {
        if (!$(this).is(':visible')) {
          $(this).prop('required', false);
        }
      });
  }
}

function toogleFormset(selectElement, value = null, formsetToShow, formsetToHide) {
  if (selectElement) {
    $(document).on('change', selectElement, function () {
      const selectedValue = $(this).val();
      //console.log("Selected value: ", selectedValue);
      if (selectedValue === value) {
        $(formsetToShow).show();
        $(formsetToHide).hide();
      } else if (selectedValue === '1' || selectedValue === '2') {
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

// function disabledCSS
function disabledCSS(el) {
  el.css({
    'background-color': '#e9ecef',
    'pointer-events': 'none',
    opacity: '1'
  });
}

// for file upload
$(document).on('change', 'input[type="file"][multiple]', function () {
  const count = this.files.length;
  const label = $(this).siblings('.file-upload-label');

  if (count === 0) {
    label.text('0 fich.');
  } else if (count === 1) {
    label.text('1 fich.');
  } else {
    label.text(`${count} fich.`);
  }
});

// functions for collecte js class
// getting values method
function getValue(fieldId) {
  const field = document.getElementById(fieldId);
  return field ? field.value : null;
}

// getting checkbox value for yes or no
function getCheckboxValueYesNo(fieldId) {
  const container = $('#' + fieldId);
  const ouiChecked = container.find('[data-field=' + fieldId + '-oui]').is(':checked');
  const nonChecked = container.find('[data-field=' + fieldId + '-non]').is(':checked');
  if (ouiChecked) {
    return true;
  } else if (nonChecked) {
    return false;
  }
  return null;
}

// getting value for simple checkbox
function getCheckboxValue(fieldId) {
  const checkbox = document.getElementById(fieldId);
  console.log(checkbox);
  return checkbox ? checkbox.checked : false;
}

// ✅ Fonction utilitaire pour convertir un fichier en base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      resolve(reader.result);
    };
    reader.onerror = error => {
      reject(error);
    };
    reader.readAsDataURL(file);
  });
}
// ✅ Fonction récursive pour aplatir les erreurs imbriquées
function flattenErrors(errors, prefix = '') {
  const flatErrors = [];
  Object.entries(errors).forEach(([field, value]) => {
    const fullField = prefix ? `${prefix}.${field}` : field;
    // ✅ CAS 1 : tableau
    if (Array.isArray(value)) {
      value.forEach((item, index) => {
        // ➜ tableau de strings (cas simple)
        if (typeof item === 'string') {
          flatErrors.push({
            field: fullField,
            message: item
          });
        }
        // ➜ tableau d'objets (cas DRF imbriqué)
        else if (typeof item === 'object' && item !== null) {
          flatErrors.push(...flattenErrors(item, `${fullField}[${index}]`));
        }
      });
    }
    // ✅ CAS 2 : objet imbriqué
    else if (typeof value === 'object' && value !== null) {
      flatErrors.push(...flattenErrors(value, fullField));
    }
    // ✅ CAS 3 : valeur simple
    else {
      flatErrors.push({
        field: fullField,
        message: value
      });
    }
  });
  return flatErrors;
}

// ✅ Notification discrète (toast)
function showNotification(message, type = 'info') {
  const toastHtml = `
    <div class="toast align-items-center text-white bg-${type} border-0 position-fixed top-0 end-0 m-3"
      role="alert"
      style="z-index: 9999;">
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', toastHtml);
  const toastElement = document.querySelector('.toast:last-child');
  const toast = new bootstrap.Toast(toastElement, { delay: 3000 });
  toast.show();
  // Supprimer après affichage
  toastElement.addEventListener('hidden.bs.toast', () => {
    toastElement.remove();
  });
}
// Utilitaires
function getCsrfToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}
// message an ux tips
function showLoader(form = null) {
  // Afficher un message de chargement ou une animation
  if (!form) {
    showNotification('Chargement des informations...', 'info');
  }
  // Afficher un spinner ou désactiver le bouton de soumission pour indiquer que le formulaire est en cours de traitement
  if (form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Enregistrement...';
  }
}
