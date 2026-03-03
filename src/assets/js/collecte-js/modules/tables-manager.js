import { FormUtils } from './form-utils.js';

export class DynamicTableManager {
  constructor(config) {
    const {
      tbodyId,
      addButtonId,
      tableId,
      rowPrefix,
      fields,
      autoAdd = true,
      minRows = 1,
      showRowNumber = false,
      toggleChecker = null,
      customTemplate = null,
      onRowCreated = null,
      customCollectData = null
    } = config;

    this.tbodyId = tbodyId;
    this.addButtonId = addButtonId;
    this.tableId = tableId;
    this.rowPrefix = rowPrefix;
    this.fields = fields;
    this.autoAdd = autoAdd;
    this.minRows = minRows;
    this.showRowNumber = showRowNumber;
    this.toggleChecker = toggleChecker;
    this.customTemplate = customTemplate;
    this.onRowCreated = onRowCreated;
    this.customCollectData = customCollectData;

    this.rowCounter = 0;
    this.$tbody = $(`#${tbodyId}`);
    this.$table = $(`#${tableId}`);
    this.$addButton = $(`#${addButtonId}`);

    this._bindEvents();
    this.addNewRow();
  }

  // ─── Template ────────────────────────────────────────────────────────────────

  _getRowTemplate(rowId) {
    if (this.customTemplate) {
      return this.customTemplate(rowId, this.rowPrefix);
    }

    let rowHtml = `<tr class="dynamic-row" data-row-id="${rowId}">`;

    if (this.showRowNumber) {
      rowHtml += `<td class="text-center p-0 row-number">${rowId}</td>`;
    }

    this.fields.forEach(field => {
      rowHtml += `<td class="p-0">`;

      if (field.type === 'select2') {
        rowHtml += `
          <select style="width: 300px !important;"
            class="form-select form-select-sm select2-ajax dynamic-field"
            name="${this.rowPrefix}_${rowId}_${field.name}"
            data-ajax-url="${field.ajaxUrl}"
            data-ajax-placeholder="${field.placeholder || 'Rechercher...'}"
            data-field="${field.name}"
            data-ajax-length="2">
          </select>`;
      } else if (field.type === 'checkbox-group') {
        rowHtml += `<div class="d-flex gap-1 checkbox-group" data-field="${field.name}">`;
        field.options.forEach((option, index) => {
          rowHtml += `
            <input type="checkbox"
              class="form-check-input month-checkbox"
              name="${this.rowPrefix}_${rowId}_${field.name}_${index}"
              value="${option.value}"
              data-month="${option.value}">`;
        });
        rowHtml += `</div>`;
      } else if (['text', 'date', 'number'].includes(field.type)) {
        const readonly = field.readonly ? 'readonly' : '';
        const extraClass = field.className || '';
        rowHtml += `
          <input type="${field.type}"
            class="form-control form-control-sm dynamic-field ${extraClass}"
            name="${this.rowPrefix}_${rowId}_${field.name}"
            placeholder="${field.placeholder || ''}"
            ${field.settings || ''}
            data-field="${field.name}"
            ${readonly}>`;
      }

      rowHtml += `</td>`;
    });

    rowHtml += `
      <td class="p-0">
        <div class="btn-group btn-group-sm" role="group">
          <button type="button" class="btn btn-outline-danger delete-row" title="Supprimer une ligne">
            <i class="bx bx-trash"></i>
          </button>
        </div>
      </td>
    </tr>`;

    return rowHtml;
  }

  // ─── Rows ─────────────────────────────────────────────────────────────────────

  _updateRowNumbers() {
    if (this.showRowNumber) {
      this.$tbody.find('.dynamic-row').each(function (index) {
        $(this)
          .find('.row-number')
          .text(index + 1);
      });
    }
  }

  addNewRow() {
    this.rowCounter++;
    const $newRow = $(this._getRowTemplate(this.rowCounter));
    this.$tbody.append($newRow);
    this._updateRowNumbers();

    setTimeout(() => {
      FormUtils.initSelect2Ajax($newRow, this.rowPrefix);

      if (this.onRowCreated) {
        this.onRowCreated($newRow, this.rowCounter);
      }
      if (this.toggleChecker) {
        this.toggleChecker(this.rowCounter);
      }

      $newRow.find('input:first, select:first').focus();
    }, 100);

    return $newRow;
  }

  clearAllRows() {
    this.$tbody.find('.dynamic-row').each(function () {
      $(this)
        .find('.select2-ajax')
        .each(function () {
          if ($(this).hasClass('select2-hidden-accessible')) {
            $(this).select2('destroy');
          }
        });
    });
    this.$tbody.empty();
    this.rowCounter = 0;
  }

  // ─── Validation ──────────────────────────────────────────────────────────────

  _isRowComplete($row) {
    let isComplete = true;
    $row.find('.dynamic-field').each(function () {
      if (!$(this).val()?.trim()) {
        isComplete = false;
        return false;
      }
    });
    return isComplete;
  }

  _hasEmptyRow() {
    let hasEmpty = false;
    this.$tbody.find('.dynamic-row').each((_, row) => {
      if (!this._isRowComplete($(row))) {
        hasEmpty = true;
        return false;
      }
    });
    return hasEmpty;
  }

  // ─── Collect ─────────────────────────────────────────────────────────────────

  async collectData() {
    if (this.customCollectData && typeof this.customCollectData === 'function') {
      return this.customCollectData();
    }

    const data = [];
    this.$tbody.find('.dynamic-row').each((_, row) => {
      const $row = $(row);
      const rowId = $row.data('row-id');
      const rowData = {};

      this.fields.forEach(field => {
        if (field.type === 'checkbox-group') {
          const checkedValues = [];
          $row.find(`[data-field="${field.name}"]:checked`).each(function () {
            checkedValues.push({ mois_numero: parseInt($(this).val()), statut: true });
          });
          rowData[field.name] = checkedValues;
        } else {
          rowData[field.name] = $row.find(`[name="${this.rowPrefix}_${rowId}_${field.name}"]`).val();
        }
      });

      const hasData = Object.values(rowData).some(v => {
        if (Array.isArray(v)) return v.length > 0;
        return v && v.toString().trim() !== '';
      });

      if (hasData) data.push(rowData);
    });

    return data;
  }

  // ─── Events ──────────────────────────────────────────────────────────────────

  _bindEvents() {
    if (this.autoAdd) {
      this.$tbody.on('change blur', '.dynamic-field', e => {
        const $row = $(e.target).closest('.dynamic-row');
        if (this._isRowComplete($row) && !this._hasEmptyRow()) {
          setTimeout(() => this.addNewRow(), 100);
        }
      });
    }

    this.$addButton.on('click', () => this.addNewRow());

    this.$tbody.on('click', '.delete-row', e => {
      const $row = $(e.target).closest('.dynamic-row');
      const rowCount = this.$tbody.find('.dynamic-row').length;

      if (rowCount > this.minRows) {
        $row.find('.select2-ajax').each(function () {
          if ($(this).hasClass('select2-hidden-accessible')) {
            $(this).select2('destroy');
          }
        });
        $row.remove();
        this._updateRowNumbers();
      } else {
        $row.find('.dynamic-field').each(function () {
          $(this).hasClass('select2-ajax') ? $(this).val(null).trigger('change') : $(this).val('');
        });
      }
    });
  }
}
