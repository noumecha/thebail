function getCSRFToken(formWrapper = null) {
  if (formWrapper) {
    const token = $('#' + formWrapper)
      .find('input[name="csrfmiddlewaretoken"]')
      .val();
    if (token) return token;
  }
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith('csrftoken=')) {
      return cookie.substring('csrftoken='.length);
    }
  }
  return '';
}

function updateHidden(value, hiddenId) {
  $('#' + hiddenId).val(value);
}

function toggleCheck({
  listId,
  checkbox,
  dynamicCheckClass,
  dynamicOptionClass,
  dynamicInputClass,
  doubleUnchecked = false,
  hiddenId,
  onToggle = null
}) {
  const $list = $('#' + listId);
  const $cb = $(checkbox);
  const label = $cb.val();

  const $container = $cb.closest('.' + dynamicOptionClass);
  const $xInput = $container.find('.' + dynamicInputClass);

  // 1️⃣ décocher les autres
  $list
    .find('.' + dynamicCheckClass)
    .not($cb)
    .prop('checked', false)
    .closest('.' + dynamicOptionClass)
    .find('.' + dynamicInputClass)
    .addClass('d-none');

  // 2️⃣ lorsque l'option cochée est décoché on coche l'autre option (oui/non) et si l'option doubleUnchecked est défini
  if (!$cb.is(':checked') && doubleUnchecked) {
    // Récupérer l'autre checkbox qui vient d'être cochée
    const $otherCb = $list.find('.' + dynamicCheckClass).not($cb);
    $otherCb
      .prop('checked', true)
      .closest('.' + dynamicOptionClass)
      .find('.' + dynamicInputClass)
      .removeClass('d-none');

    // ✅ Appeler onToggle avec les valeurs de l'AUTRE checkbox (celle qui vient d'être activée)
    onToggle && onToggle(true, $otherCb.val());
  } else {
    $xInput.removeClass('d-none').focus();
    onToggle && onToggle($cb.is(':checked'), label);
  }

  if (hiddenId) {
    const value = $cb.is(':checked') ? label : '';
    updateHidden(value, hiddenId);
  }
}

function initDynamicChoiceList(listId, hiddenId, newInputId, formWrapper, addBtnId, url) {
  const $list = $('#' + listId);

  $list.on('change', '.dynamic-check', function () {
    toggleCheck({
      listId: listId,
      checkbox: this,
      dynamicCheckClass: 'dynamic-check',
      dynamicOptionClass: 'dynamic-option',
      dynamicInputClass: 'dynamic-x-input',
      hiddenId: hiddenId
    });
  });

  // save option to db and add to the list
  $('#' + addBtnId).click(function () {
    try {
      const val = $('#' + newInputId)
        .val()
        .trim();
      if (!val) return;
      console.log('token: ', getCSRFToken(formWrapper));
      console.log('list id ', listId);
      console.log('data sent: ', { label: val, model: $('#' + listId).data('model') });
      if (url) {
        $.post({
          url: url,
          data: {
            label: val,
            model: $('#' + listId).data('model')
          },
          headers: {
            'X-CSRFToken': getCSRFToken(formWrapper)
          }
        })
          .done(function (res) {
            addToList(res.id, res.label, listId);
          })
          .fail(function (xhr) {
            if (xhr.status === 409) {
              let errorBlock = $(`#${listId}-alert-block`);
              let errorMessage = $(errorBlock).find('.error-message');
              errorBlock.toggleClass('d-none');
              errorMessage.text('Ce libellé existe déjà.');
              setTimeout(() => {
                errorBlock.toggleClass('d-none');
              }, 3000);
            }
          });
      } else {
        addToList(null, val, listId);
      }
      $('#' + newInputId).val('');
    } catch (error) {
      console.log('error : ', error);
    }
  });
}

function addToList(id, label, listId) {
  const $label = $(`
      <label class="d-flex align-items-center gap-2 dynamic-option">
        <input type="checkbox"
          name="${listId}_checkbox"
          value="${id || label}"
          class="form-check-input dynamic-check">
        <span class="fw-bold">${label}</span>
      </label>
    `);

  $list = $('#' + listId);
  $list.append($label);
  $label.find('.dynamic-check').change();
}
