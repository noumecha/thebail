function initDynamicChoiceList(listId, hiddenId, newInputId, addBtnId) {
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

  // add new option
  $('#' + addBtnId).click(function () {
    const val = $('#' + newInputId)
      .val()
      .trim();
    if (!val) return;
    const $label = $(`
      <label class="d-flex align-items-center gap-2 dynamic-option">
        <input type="checkbox" name="${listId}_checkbox" value="${val}" class="form-check-input dynamic-check">
        <span class="fw-bold">${val}</span>
      </label>
    `);
    $list.append($label);
    $label.find('.dynamic-check').change();
    $('#' + newInputId).val('');
  });
}

// init examples
$(function () {
  initDynamicChoiceList(
    'construction-list',
    'construction-choice-hidden',
    'new-construction-input',
    'add-construction-btn'
  );
  initDynamicChoiceList(
    'type-location-list',
    'type-location-choice-hidden',
    'new-type-location-input',
    'add-type-location-btn'
  );
});
