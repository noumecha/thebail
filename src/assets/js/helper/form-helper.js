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

function initDynamicChoiceList(listId, hiddenId, newInputId, addBtnId, url) {
  const $list = $('#' + listId);
  const $hidden = $('#' + hiddenId);

  function updateHidden(value) {
    $hidden.val(value);
  }

  $list.on('change', '.dynamic-check', function () {
    const $cb = $(this);
    const label = $cb.val();
    const $container = $cb.closest('.dynamic-option');
    const $xInput = $container.find('.dynamic-x-input');

    // uncheck others
    $list
      .find('.dynamic-check')
      .not($cb)
      .prop('checked', false)
      .closest('.dynamic-option')
      .find('.dynamic-x-input')
      .addClass('d-none');

    if ($xInput.length && label.includes('Etage R+')) {
      if ($cb.is(':checked')) {
        $xInput.removeClass('d-none').focus();
        $xInput.on('input', function () {
          updateHidden(`Etage R+${$(this).val()}`);
        });
      }
    } else {
      updateHidden($cb.is(':checked') ? label : '');
    }
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

// init examples
$(function () {
  initDynamicChoiceList(
    'construction-list',
    'construction-choice-hidden',
    'new-construction-input',
    'add-construction-btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'type-location-list',
    'type-location-choice-hidden',
    'new-type-location-input',
    'add-type-location-btn',
    '/add-choice/'
  );
  initDynamicChoiceList('statut-list', 'statut-choice-hidden', 'new-statut-input', 'add-statut-btn', '/add-choice/');
  initDynamicChoiceList(
    'revetementinterieure-list',
    'revetementinterieure-choice-hidden',
    'new-revetementinterieure-input',
    'add-revetementinterieure-btn',
    '/add-choice/'
  );
  initDynamicChoiceList(
    'revetementexterieure-list',
    'revetementexterieure-choice-hidden',
    'new-revetementexterieure-input',
    'add-revetementexterieure-btn',
    '/add-choice/'
  );
});
