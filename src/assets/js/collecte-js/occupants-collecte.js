$(function () {
    function resetOccupantForm() {
        $("#id_occupants_residence-0-Nom_Prenom").val("");
        $("#id_occupants_residence-0-Administration_tutelle").val("");
        $("#id_occupants_residence-0-Fonction").val("");
        $("#id_occupants_residence-0-Matricule").val("");
        $("#id_occupants_residence-0-NIU").val("");
        $("#id_occupants_residence-0-Ref_ActeJuridique").val("");
        $("#id_occupants_residence-0-Date_Signature_acte_juridique").val("");
        $("#id_occupants_residence-0-Telephone").val("");
    }

    // Lignes vides
    const $emptyRow = $("#occupant-collecte-table tbody #empty-occupant-row");

    $("#occupant-collecte-add-btn").on("click", function () {
        const nomPrenom = $("#id_occupants_residence-0-Nom_Prenom").val();
        const adminTutelle = $("#id_occupants_residence-0-Administration_tutelle").val();
        const adminTutelleText = $(`#id_occupants_residence-0-Administration_tutelle option[value='${adminTutelle}']`).text();
        const fonction = $("#id_occupants_residence-0-Fonction").val();
        const matricule = $("#id_occupants_residence-0-Matricule").val();
        const niu = $("#id_occupants_residence-0-NIU").val();
        const refActe = $("#id_occupants_residence-0-Ref_ActeJuridique").val();
        const dateActe = $("#id_occupants_residence-0-Date_Signature_acte_juridique").val();
        const telephone = $("#id_occupants_residence-0-Telephone").val();

        if (!nomPrenom) {
            alert("Veuillez saisir le nom et prénom de l’occupant.");
            return;
        }

        const row = `
            <tr data='occupant'>
                <td><input type="hidden" name="Nom_Prenom_hidden[]" value="${nomPrenom}">${nomPrenom}</td>
                <td><input type="hidden" name="Administration_tutelle_hidden[]" value="${adminTutelle}">${adminTutelleText}</td>
                <td><input type="hidden" name="Fonction_hidden[]" value="${fonction}">${fonction}</td>
                <td>
                    <input type="hidden" name="Matricule_hidden[]" value="${matricule}">${matricule}<br>
                    <input type="hidden" name="NIU_hidden[]" value="${niu}">${niu}
                </td>
                <td><input type="hidden" name="Ref_ActeJuridique_hidden[]" value="${refActe}">${refActe}</td>
                <td><input type="hidden" name="Date_Signature_acte_juridique_hidden[]" value="${dateActe}">${dateActe}</td>
                <td><input type="hidden" name="Telephone_hidden[]" value="${telephone}">${telephone}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-warning edit-occupant">Éditer</button>
                    <button type="button" class="btn btn-sm btn-danger delete-occupant">Supprimer</button>
                </td>
            </tr>
        `;

        $("#occupant-collecte-table tbody").append(row);
        $emptyRow.hide();
        resetOccupantForm();
    });

    // Supprimer une ligne
    $(document).on("click", ".delete-occupant", function () {
        $(this).closest("tr").remove();
        if ($("#occupant-collecte-table tbody tr").length === 0) {
            $emptyRow.show();
        }
    });

    // Éditer une ligne
    $(document).on("click", ".edit-occupant", function () {
        const row = $(this).closest("tr");

        $("#id_occupants_residence-0-Nom_Prenom").val(row.find('input[name="Nom_Prenom_hidden[]"]').val());
        $("#id_occupants_residence-0-Administration_tutelle").val(row.find('input[name="Administration_tutelle_hidden[]"]').val());
        $("#id_occupants_residence-0-Fonction").val(row.find('input[name="Fonction_hidden[]"]').val());
        $("#id_occupants_residence-0-Matricule").val(row.find('input[name="Matricule_hidden[]"]').val());
        $("#id_occupants_residence-0-NIU").val(row.find('input[name="NIU_hidden[]"]').val());
        $("#id_occupants_residence-0-Ref_ActeJuridique").val(row.find('input[name="Ref_ActeJuridique_hidden[]"]').val());
        $("#id_occupants_residence-0-Date_Signature_acte_juridique").val(row.find('input[name="Date_Signature_acte_juridique_hidden[]"]').val());
        $("#id_occupants_residence-0-Telephone").val(row.find('input[name="Telephone_hidden[]"]').val());
        row.remove();
        if ($('#nonmandatement-collecte-table tbody tr').length === 1) {
            $emptyRow.show();
        }
    });
});
