$(function() {
    function resetAyantDroitForm() {
        $("#id_ayants_droits-0-Nom_Prenom").val("");
        $("#id_ayants_droits-0-Contact").val("");
        $("#id_ayants_droits-0-Reference_Grosse").val("");
        $("#id_ayants_droits-0-Date_prise_effet_grosse").val("");
        $("#id_ayants_droits-0-Reference_certificat_non_effet").val("");
        $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val("");
    }

    $("#ayantdroit-collecte-add-btn").on("click", function () {
        const nomPrenom = $("#id_ayants_droits-0-Nom_Prenom").val();
        const contact = $("#id_ayants_droits-0-Contact").val();
        const grosse = $("#id_ayants_droits-0-Reference_Grosse").val();
        const dateGrosse = $("#id_ayants_droits-0-Date_prise_effet_grosse").val();
        const certificat = $("#id_ayants_droits-0-Reference_certificat_non_effet").val();
        const dateCertificat = $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val();

        if (!nomPrenom) {
            alert("Veuillez saisir le nom et prénom.");
            return;
        }

        // Clone du template
        const $template = $("#ayantdroit-template").find("tr").clone();

        $template.find(".nom-prenom").text(nomPrenom);
        $template.find(".contact").text(contact);
        $template.find(".grosse").text(grosse);
        $template.find(".date-grosse").text(dateGrosse);
        $template.find(".certificat").text(certificat);
        $template.find(".date-certificat").text(dateCertificat);

        // Sauvegarde les données dans des attributs pour la réédition
        $template.data("form-values", {
            nomPrenom,
            contact,
            grosse,
            dateGrosse,
            certificat,
            dateCertificat
        });

        // Ajout dans le tableau
        const $tbody = $("#ayantdroit-collecte-table tbody");
        const $emptyRow = $tbody.find("tr:contains('Aucun ayant droit')");
        if ($emptyRow.length) {
            $emptyRow.remove();
        }
        $tbody.append($template);

        resetAyantDroitForm();
    });

    // Suppression
    $(document).on("click", ".ayantdroit-entry .btn-delete", function () {
        $(this).closest("tr").remove();

        // Si tableau vide, remettre ligne vide
        const $tbody = $("#ayantdroit-collecte-table tbody");
        if ($tbody.find("tr").length === 0) {
            $tbody.append(`
                <tr>
                    <td colspan="7">Aucun ayant droit du bailleur ajouté ...</td>
                </tr>
            `);
        }
    });

    // Édition
    $(document).on("click", ".ayantdroit-entry .btn-edit", function () {
        const $row = $(this).closest("tr");
        const data = $row.data("form-values");

        $("#id_ayants_droits-0-Nom_Prenom").val(data.nomPrenom);
        $("#id_ayants_droits-0-Contact").val(data.contact);
        $("#id_ayants_droits-0-Reference_Grosse").val(data.grosse);
        $("#id_ayants_droits-0-Date_prise_effet_grosse").val(data.dateGrosse);
        $("#id_ayants_droits-0-Reference_certificat_non_effet").val(data.certificat);
        $("#id_ayants_droits-0-Date_prise_effet_certificat_non_effet").val(data.dateCertificat);

        $row.remove();
    });
});
