$(function () {
    function resetNonMandatementForm() {
        $('#id_non_mandatements-0-Exercice').select2({
            placeholder : "Selectionnez un exercice",
            allowClear: true,
        })
        $("#id_non_mandatements-0-Loyer_Mensuel").val("");
        $("#id_non_mandatements-0-Ref_Attestattion").val("");
        $("#id_non_mandatements-0-Montant_total_exercice").val("");
        $("#id_non_mandatements-0-Visa_budgétaire").val("");
        $("#id_non_mandatements-0-Ref_contrat_avenant").val("");

        const mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"];
        mois.forEach(mois => {
            $(`#id_non_mandatements-0-${mois}`).prop('checked', false);
        });
    }

    // objet pour la sauvegarde globale en base de données ---> creer un Array d'objet NonMandatement à soumettre via ajax
    const NonMandatement = {
        exercice : '',
        loyer : '',
        refAttestation : '',
        montantTotal : '',
        visa : '',
        refContrat : '',
        moisList : {}
    }

    // prefix des ids 
    const prefix = "#id_non_mandatements-0-";

    // Lignes vides
    const $emptyRow = $("#nonmandatement-collecte-table tbody #empty-ayantdroit-row");

    // listes des mois
    const moisList = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"];

    // pour le calcule automatique du montant total 
    const monTantTotal = $(`${prefix}Montant_total_exercice`);
    monTantTotal.attr('disabled', true);

    // Function to calculate and update the total amount
    function updateTotalAmount() {
        const montantMensuel = parseFloat($(`${prefix}Loyer_Mensuel`).val()) || 0;
        let checkedMonths = 0;
        moisList.forEach(mois => {
            if ($(`${prefix}${mois}`).is(":checked")) {
                checkedMonths ++;
            }
        });
        const total = checkedMonths * montantMensuel;
        monTantTotal.val(total.toFixed(2));
    }

    // Listen for changes on montantMensuel input
    moisList.forEach(mois => {
        $(`${prefix}${mois}`).on('change', function() {
            updateTotalAmount();
        });
    });
    $(`${prefix}Loyer_Mensuel`).on('input', function() {
        updateTotalAmount();
    });

    updateTotalAmount();

    $("#nonmandatement-collecte-add-btn").on("click", function () {
        const exercice = $(`${prefix}Exercice`).val();
        const exerciceText = $(`${prefix}Exercice option[value='${exercice}']`).text();
        const loyer = $(`${prefix}Loyer_Mensuel`).val();
        const refAttestation = $(`${prefix}Ref_Attestattion`).val();
        const montantTotal = $(`${prefix}Montant_total_exercice`).val();
        const visa = $(`${prefix}Visa_budgétaire`).val();
        const refContrat = $(`${prefix}Ref_contrat_avenant`).val();

        const moisList = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"];
        let moisCoches = [];
        let moisHiddenInputs = '';

        moisList.forEach(mois => {
            const checked = $(`${prefix}${mois}`).is(":checked");
            moisCoches.push(checked ? "✔️" : "❌");
            moisHiddenInputs += `<input type="hidden" name="${mois}_hidden[]" value="${checked ? '1' : '0'}">`;
        });

        if (!exercice || !loyer) {
            alert("Veuillez remplir au moins l'exercice et le loyer mensuel.");
            return;
        }

        let row = `
            <tr>
                <td><input type="hidden" name="Exercice_hidden[]" value="${exercice}">${exerciceText}</td>
                <td><input type="hidden" name="Loyer_hidden[]" value="${loyer}">${loyer}</td>
                <td><input type="hidden" name="Ref_Attestattion_hidden[]" value="${refAttestation}">${refAttestation}</td>
                ${moisList.map((mois, index) => `<td>${moisCoches[index]}</td>`).join('')}
                ${moisHiddenInputs}
                <td><input type="hidden" name="Montant_total_hidden[]" value="${montantTotal}">${montantTotal}</td>
                <td><input type="hidden" name="Visa_hidden[]" value="${visa}">${visa == true ? "oui" : "non"}</td>
                <td><input type="hidden" name="Ref_contrat_hidden[]" value="${refContrat}">${refContrat}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-warning edit-nonmandatement">Éditer</button>
                    <button type="button" class="btn btn-sm btn-danger delete-nonmandatement">Supprimer</button>
                </td>
            </tr>
        `;

        $('#nonmandatement-collecte-table tbody').append(row);
        $emptyRow.hide();
        resetNonMandatementForm();
    });

    // Supprimer une ligne
    $(document).on('click', '.delete-nonmandatement', function () {
        $(this).closest('tr').remove();

        if ($('#nonmandatement-collecte-table tbody tr').length === 1) {
            $emptyRow.show();
        }
    });

    // Éditer une ligne
    $(document).on("click", ".edit-nonmandatement", function () {
        const prefix = "#id_non_mandatements-0-";
        const row = $(this).closest("tr");

        $(`${prefix}Exercice`).val(row.find('input[name="Exercice_hidden[]"]').val());
        $(`${prefix}Loyer_Mensuel`).val(row.find('input[name="Loyer_hidden[]"]').val());
        $(`${prefix}Ref_Attestattion`).val(row.find('input[name="Ref_Attestattion_hidden[]"]').val());
        $(`${prefix}Date_signature`).val(row.find('input[name="Date_signature_hidden[]"]').val());
        $(`${prefix}Montant_total_exercice`).val(row.find('input[name="Montant_total_hidden[]"]').val());
        $(`${prefix}Visa_budgétaire`).val(row.find('input[name="Visa_hidden[]"]').val());
        $(`${prefix}Ref_contrat_avenant`).val(row.find('input[name="Ref_contrat_hidden[]"]').val());
        $(`${prefix}Etat`).val(row.find('input[name="Etat_hidden[]"]').val());

        const moisList = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"];
        moisList.forEach(mois => {
            const val = row.find(`input[name="${mois}_hidden[]"]`).val();
            $(`${prefix}${mois}`).prop('checked', val === "1");
        });

        row.remove();

        if ($('#nonmandatement-collecte-table tbody tr').length === 1) {
            $emptyRow.show();
        }
    });
});
