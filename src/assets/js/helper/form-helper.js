function getCSRFToken() {
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

function toggleCheck({ listId, checkbox, dynamicCheckClass, dynamicOptionClass, dynamicInputClass, hiddenId }) {
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

  // 2️⃣ logique métier
  if ($cb.is(':checked') && $xInput.length && label.includes('Etage R+')) {
    $xInput.removeClass('d-none').focus();

    // évite les handlers multiples
    $xInput.off('input').on('input', function () {
      updateHidden(`Etage R+${$(this).val()}`, hiddenId);
    });
  } else {
    updateHidden($cb.is(':checked') ? label : '', hiddenId);
    $xInput.addClass('d-none');
  }
}

function initDynamicChoiceList(listId, hiddenId, newInputId, addBtnId, url) {
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
    const val = $('#' + newInputId)
      .val()
      .trim();
    if (!val) return;
    if (url) {
      $.post({
        url: url,
        data: {
          label: val,
          model: $('#' + listId).data('model')
        },
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      }).done(function (res) {
        addToList(res.id, res.label, listId);
      });
    } else {
      addToList(null, val, listId);
    }
    $('#' + newInputId).val('');
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
