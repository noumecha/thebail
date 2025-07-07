$(function () {
    const modal = $('#create-typecontrat-modal');
    const formContainer = $('#typecontrat-form-content');
    const successAlert = $('#modal-form-alert-success');
    const errorAlert = $('#modal-form-alert-errors');

    // load form with data
    $(document).on('click', '[data-bs-target="#create-typecontrat-modal"]', function () {
        $.get("/contrat/types/form/", function (data) {
            formContainer.html(data.html);
        });
    });
    // submit the form
    $(document).on('submit', '#typeContratForm', function (e) {
        e.preventDefault();
        const form = $(this);
        const formData = form.serialize();
        // send ajax request
        $.ajax({
            url: "/contrat/types/form/",
            type: 'POST',
            data: formData,
            success: function (data) {
                if (data.success) {
                    window.location.reload();
                    modal.hide();
                    successAlert.removeClass('d-none').text(data.message);
                } else {
                    console.log("error happen", data);
                }
            }
        });
    });
});
