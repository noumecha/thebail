$(function () {
    const modal = new bootstrap.Modal($('#create-typecontrat-modal')[0]);
    const formContainer = $('#typecontrat-form-content');
    const form = $('#typeContratForm');
    const successAlert = $('#modal-form-alert-success');
    const errorAlert = $('#modal-form-alert-errors');

    // Charger formulaire (création ou update)
    $(document).on('click', '[data-action="open-typecontrat-modal"]', function () {
        const url = $(this).data('url');

        $.get(url, function (data) {
            formContainer.html(data);
            modal.show();
        });
    });

    // Soumettre le formulaire (create/update)
    form.on('submit', function (e) {
        e.preventDefault();

        const actionUrl = form.find('form').attr('action') || "{% url 'type_contrat_create_form' %}";
        const formData = form.find('form').serialize();

        $.ajax({
            url: actionUrl,
            type: 'POST',
            data: formData,
            success: function (data) {
                if (data.success) {
                    location.reload(); // Ou mettre à jour le DOM via JS
                } else {
                    formContainer.html(data.html);
                }
            }
        });
    });

    // Supprimer
    $(document).on('click', '.delete-typecontrat', function () {
        if (!confirm("Voulez-vous vraiment supprimer ce type de contrat ?")) return;

        const url = $(this).data('url');

        $.post(url, {'csrfmiddlewaretoken': '{{ csrf_token }}'}, function (data) {
            if (data.success) {
                location.reload(); // Ou retirer la ligne du DOM
            }
        });
    });
});
