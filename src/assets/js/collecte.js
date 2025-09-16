$(function () {
    // set visibility on modal load initialization
    setVisible('id_immeubles-0-Type_localisation', '#id_Ville, #id_Rue', '1') // 1 - Extérieure
    setVisible('id_immeubles-0-Type_localisation', '#id_region, #id_departement, #id_arrondissement, #id_Quartier', '2') // 2 - National

    // toggle occupants visibility 
    toogleFormset("#id_Type_location", "2", '#batiment_occ_residence-0', '#batiment_occ_bureaux-0')
    toogleFormset("#id_Type_location", "1", '#batiment_occ_bureaux-0', '#batiment_occ_residence-0')

    // select 2 widget 
    $('#id_TypeContrat').select2({
        placeholder : "Selectionnez un Type de Contrat",
        allowClear: true,
    })
    $('#id_immeubles-0-Revetement_interieure').select2({
        placeholder : "Selectionnez un revetement intérieure",
        allowClear: true,
    })
    $('#id_immeubles-0-Revetement_exterieure').select2({
        placeholder : "Selectionnez un revetement extérieure",
        allowClear: true,
    })
    $('#id_non_mandatements-0-Exercice').select2({
        placeholder : "Selectionnez un exercice",
        allowClear: true,
    })

    /****  for inside form modal ***/
    // typecontrat
    ajaxModal("#addTypeContratModal", "#typecontrat-form-content", "#typecontratForm", "/type-contrat-partial-form/", "#id_TypeContrat")
    // revetementint-partial-form/, revetementext-partial-form/
    ajaxModal("#addRevetementInterieureModal", "#revetementint-form-content", "#revetementintForm", "/revetementint-partial-form/", "#id_immeubles-0-Revetement_interieure")
    ajaxModal("#addRevetementExterieureModal", "#revetementext-form-content", "#revetementextForm", "/revetementext-partial-form/", "#id_immeubles-0-Revetement_exterieure")
    ajaxModal("#addExerciceModal", "#exercice-form-content", "#exerciceForm", "/exercice-partial-form/", "#id_non_mandatements-0-Exercice")

    /** hidden & show elements */
    // set visibility for type localisation
    setVisible('#id_immeubles-0-Type_localisation', '#id_immeubles-0-Ville, #id_immeubles-0-pays, #id_immeubles-0-Rue', '1') // 1 - Extérieure
    setVisible('#id_immeubles-0-Type_localisation', '#id_immeubles-0-region,  #id_immeubles-0-departement, #id_immeubles-0-arrondissement, #id_immeubles-0-Quartier', '2') // 2 - National

    // set visibility for type personne
    setVisible('#id_bailleurs-0-Type_personne', '#id_bailleurs-0-Nom_prenom, #id_bailleurs-0-Maticule, #id_bailleurs-0-Type_id_bailleur, #id_bailleurs-0-Num_doc, #id_bailleurs-0-Date_delivrance_doc, #id_bailleurs-0-Document_identification', '2') // 2 - personne physique
    setVisible('#id_bailleurs-0-Type_personne', '#id_bailleurs-0-Raison_social', '1') // 1 - personne morale 

    // toggle occupants visibility 
    toogleFormset("#id_immeubles-0-Type_location", "2", '#occupants_residence-0', '#occupants_bureau-0')
    toogleFormset("#id_immeubles-0-Type_location", "1", '#occupants_bureau-0', '#occupants_residence-0')

    // process to the data saving : 
    $(document).on("click", "#submit-id-save", function (e) {
            e.preventDefault();
            let formData = new FormData($("#collecte-form")[0]);
            // avenants
            let avenants = [];
            let ayants_droits = [];
            $('#avenant-collecte-list .avenant-entry').each(function () {
                let data = $(this).data('avenant');
                avenants.push(data); // Chaque data est un objet avenant
            });
            $('#ayantdroit-collecte-table tbody .ayantdroit-entry').each(function () {
                let data = $(this).data('ayantdroit'); // Assure-toi que .data('ayantdroit') contient un objet JS
                if (data) {
                    ayants_droits.push(data);
                }
            });
            console.log(ayants_droits);
            formData.append('avenants_data', JSON.stringify(avenants));
            formData.append('ayants_droits_data', JSON.stringify(ayants_droits));
            /*$.ajax({
                url: "/collecte/create",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    alert("Collecte enregistrée avec succès !");
                    showAlertMessage(response.message, '#form-success-collecte')
                },
                error: function (xhr, status, error) {
                    let errors = xhr.responseJSON.errors;
                    console.log(errors);
                    showAlertMessage(errors, '#form-error-collecte')
                }
            });*/
    });
})