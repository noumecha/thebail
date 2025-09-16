$(function () {
    function resetOccupantBureauForm() {
        $("#id_occupants_bureau-0-Service").val("");
        $("#id_occupants_bureau-0-Administration_correspondante").val("");
        $("#id_occupants_bureau-0-Fonction").val("");
        $("#id_occupants_bureau-0-Ref_ActeJuridique_attribution").val("");
        $("#id_occupants_bureau-0-Contact").val("");
        $("#id_occupants_bureau-0-Date_initial_acte_occupation").val("");
        $("#id_occupants_bureau-0-Immeuble").val("");
    }

    const $emptyRow = $("#occupantbureau-collecte-table tbody #empty-occupantbureau-row");

    $("#occupantbureau-collecte-add-btn").on("click", function () {
        const service = $("#id_occupants_bureau-0-Service").val();
        const serviceText = $(`#id_occupants_bureau-0-Service option[value='${service}']`).text();
        const adminCorr = $("#id_occupants_bureau-0-Administration_correspondante").val();
        const fonction = $("#id_occupants_bureau-0-Fonction").val();
        const refActe = $("#id_occupants_bureau-0-Ref_ActeJuridique_attribution").val();
        const contact = $("#id_occupants_bureau-0-Contact").val();
        const dateOccupation = $("#id_occupants_bureau-0-Date_initial_acte_occupation").val();
        const immeuble = $("#id_occupants_bureau-0-Immeuble").val();

        if (!service) {
            alert("Veuillez saisir le nom du service.");
            return;
        }

        const row = `
            <tr>
                <td><input type="hidden" name="Service_hidden[]" value="${service}">${serviceText}</td>
                <td><input type="hidden" name="Administration_correspondante_hidden[]" value="${adminCorr}">${adminCorr}</td>
                <td><input type="hidden" name="Fonction_hidden[]" value="${fonction}">${fonction}</td>
                <td><input type="hidden" name="Ref_ActeJuridique_attribution_hidden[]" value="${refActe}">${refActe}</td>
                <td><input type="hidden" name="Contact_hidden[]" value="${contact}">${contact}</td>
                <td><input type="hidden" name="Date_initial_acte_occupation_hidden[]" value="${dateOccupation}">${dateOccupation}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-warning edit-occupantbureau">Éditer</button>
                    <button type="button" class="btn btn-sm btn-danger delete-occupantbureau">Supprimer</button>
                </td>
            </tr>
        `;

        $("#occupantbureau-collecte-table tbody").append(row);
        $emptyRow.hide();
        resetOccupantBureauForm();
    });

    // Supprimer une ligne
    $(document).on("click", ".delete-occupantbureau", function () {
        $(this).closest("tr").remove();
        if ($("#occupantbureau-collecte-table tbody tr").length === 0) {
            $emptyRow.show();
        }
    });

    // Éditer une ligne
    $(document).on("click", ".edit-occupantbureau", function () {
        const row = $(this).closest("tr");

        $("#id_occupants_bureau-0-Service").val(row.find('input[name="Service_hidden[]"]').val());
        $("#id_occupants_bureau-0-Administration_correspondante").val(row.find('input[name="Administration_correspondante_hidden[]"]').val());
        $("#id_occupants_bureau-0-Fonction").val(row.find('input[name="Fonction_hidden[]"]').val());
        $("#id_occupants_bureau-0-Ref_ActeJuridique_attribution").val(row.find('input[name="Ref_ActeJuridique_attribution_hidden[]"]').val());
        $("#id_occupants_bureau-0-Contact").val(row.find('input[name="Contact_hidden[]"]').val());
        $("#id_occupants_bureau-0-Date_initial_acte_occupation").val(row.find('input[name="Date_initial_acte_occupation_hidden[]"]').val());
        $("#id_occupants_bureau-0-Immeuble").val(row.find('input[name="Immeuble_hidden[]"]').val());

        row.remove();

        if ($("#occupantbureau-collecte-table tbody tr").length === 1) {
            $emptyRow.show();
        }
    });
});
