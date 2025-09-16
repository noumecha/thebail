$(function() {
    function resetAyantDroitForm() {
        $("#id_ayants_droits-0-Nom_Prenom").val("");
        $("#id_ayants_droits-0-Contact").val("");
        $("#id_ayants_droits-0-Reference_Grosse").val("");
        $("#id_ayants_droits-0-Date_prise_effet_grosse").val("");
        $("#id_ayants_droits-0-Reference_certificat_non_effet").val("");
        $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val("");
    }
    
    // objet pour la sauvegarde globale en base de données ---> creer un Array d'objet AyantDroit à soumettre via ajax
    const AyantDroit = {
        nom_prenom: '',
        contact: '',
        reference_grosse: '',
        date_prise_effet_grosse: '',
        reference_certificat_non_effet: '',
        date_prise_effet_certificat_non_effet: ''
    }

    // default empty row
    const $emptyRow = $("#empty-ayantdroit-row");

    $("#ayantdroit-collecte-add-btn").on("click", function () {
        const nomPrenom = $("#id_ayants_droits-0-Nom_Prenom").val();
        const contact = $("#id_ayants_droits-0-Contact").val();
        const grosse = $("#id_ayants_droits-0-Reference_Grosse").val();
        const dateGrosse = $("#id_ayants_droits-0-Date_prise_effet_grosse").val();
        const certificat = $("#id_ayants_droits-0-Reference_certificat_non_effet").val();
        const dateCertificat = $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val();

        // validation du formaulre ---> à revoir 
        if (!nomPrenom) {
            alert("Veuillez saisir le nom et prénom.");
            return;
        }

        // template de ligne du tableau
        let row = `
                <tr>
                    <td><input type="hidden" name="Nom_Prenom_hidden[]" value="${nomPrenom}">${nomPrenom}</td>
                    <td><input type="hidden" name="Contact_hidden[]" value="${contact}">${contact}</td>
                    <td><input type="hidden" name="Reference_Grosse_hidden[]" value="${grosse}">${grosse}</td>
                    <td><input type="hidden" name="Date_prise_effet_grosse_hidden[]" value="${dateGrosse}">${dateGrosse}</td>
                    <td><input type="hidden" name="Reference_certificat_non_effet_hidden[]" value="${certificat}">${certificat}</td>
                    <td><input type="hidden" name="Date_prise_effet_certificat_non_effet_hidden[]" value="${dateCertificat}">${dateCertificat}</td>
                    <td>
                        <button type="button" class="btn btn-sm btn-warning edit-ayantdroit">Éditer</button>
                        <button type="button" class="btn btn-sm btn-danger delete-ayantdroit">Supprimer</button>
                    </td>
                </tr>
            `;
        // Ajouter au tableau
        $('#ayantdroit-collecte-table tbody').append(row);

        // Supprimer le message "aucun ayant droit"
        $emptyRow.hide();

        resetAyantDroitForm();
    });

    // Supprimer une ligne
    $(document).on('click', '.delete-ayantdroit', function () {
        $(this).closest('tr').remove();
        // Si plus de lignes, afficher "aucun ayant droit"
        if ($('#ayantdroit-collecte-table tbody tr').length === 0) {
            $emptyRow.show();
        }
    });

    // Édition
    $(document).on("click", ".edit-ayantdroit", function () {
        let row = $(this).closest("tr");

        $("#id_ayants_droits-0-Nom_Prenom").val(row.find('input[name="Nom_Prenom_hidden[]"]').val());
        $("#id_ayants_droits-0-Contact").val(row.find('input[name="Contact_hidden[]"]').val());
        $("#id_ayants_droits-0-Reference_Grosse").val(row.find('input[name="Reference_Grosse_hidden[]"]').val());
        $("#id_ayants_droits-0-Date_prise_effet_grosse").val(row.find('input[name="Date_prise_effet_grosse_hidden[]"]').val());
        $("#id_ayants_droits-0-Reference_certificat_non_effet").val(row.find('input[name="Reference_certificat_non_effet_hidden[]"]').val());
        $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val(row.find('input[name="Date_prise_effet_certificat_non_effet_hidden[]"]').val());
        row.remove();
    });
});
