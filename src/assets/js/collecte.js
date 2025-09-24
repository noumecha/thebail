$(function () {

    // Quand l'administration change
    $(document).on("change", "#id_occupants_bureau-0-Administration_correspondante", function () {
        var adminId = $(this).val();
        // Trouve le champ Service dans le même formset
        var serviceField = $(this).closest(".form-row").find("#id_occupants_bureau-0-Service");
        // Reconstruit l’URL de l’autocomplete avec administration_id
        var baseUrl = serviceField.data("autocomplete-light-url").split("?")[0];
        var newUrl = baseUrl + "?administration_id=" + adminId;
        // Applique l’URL mise à jour
        serviceField.attr("data-autocomplete-light-url", newUrl);
        // Réinitialise le champ Service
        serviceField.val(null).trigger("change");
    });

    // get agent name base on the selected or typed matricule
    let agent_name = $('#id_Agent_de_collecte');
    agent_name.prop('readonly', true);
    disabledCSS(agent_name);

    $(document).on('change', '#id_Agent', function () {
        let id = $(this).val();
        if (id) {
            $.ajax({
                url: '/agent/',
                data: {
                    "agent_id" : id
                },
                success: function (data) {
                    if (data.success) {
                        $('#id_Agent_de_collecte').val(data.agent);
                    } else {                        
                        console.log("Aucune donnée trouvée ...");
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error getting Agent :', error);
                }
            });
        }
    })

    // select arrondissement and set other localisation informations automatically
    let region = $('#id_immeubles-0-region');
    let dpt = $('#id_immeubles-0-departement');
    let numero_collecte = $('#id_Numero_fiche_de_collecte')

    region.prop('readonly', true);
    dpt.prop('readonly', true);
    numero_collecte.prop('readonly', true);
    disabledCSS(region);
    disabledCSS(dpt);
    disabledCSS(numero_collecte);

    $(document).on('change',  '#id_immeubles-0-arrondissement', function () {
        let arrondissement_id = $(this).val();
        $.ajax({
            url: '/arrondissement/',
            data: {
                'arrondissement_id': arrondissement_id
            },
            success: function (data) {
                if (data.success) {
                    region.val(data.region_id);
                    dpt.val(data.dpt_id);
                    numero_collecte.val(data.numero_collecte);
                } else {
                    console.log("Aucune donnée trouvée ...");
                }
            },
            error: function(xhr, status, error) {
                console.error('Error getting data :', error);
            }
        })
    });

    // disable and enable the contrat type button by default 
    $('#id-add-contrat-type').hide();
    if ($('#id_TypeContrat')) {
        $(document).on('change', '#id_TypeContrat', function() {
            const selectedValue = $('#id_TypeContrat option:selected').text();
            console.log(selectedValue)
            if (selectedValue === "Contrat CONTRAT MINDCAF-AUTRE") {
                $('#id-add-contrat-type').show();
            } else {
                $('#id-add-contrat-type').hide();
            }
        });
        $('#id_TypeContrat').trigger('change');
    } else {
        $('#id_TypeContrat').show();
    }
    

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
    $('#id_Bailleur').select2({
        placeholder : "Selectionnez un Bailleur",
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
    ajaxModal("#addBailleurModal", "#bailleur-form-content", "#bailleurForm", "/bailleur-partial-form/", "#id_Bailleur")

    // handle the show/hide logic
    var avenantsForm = $('#avenants-0');
    var titleForm = $('#avenant-collecte-form-title');
    var checkbox = $('#id_Existance_avenant_0');
    function toggleElements() {
        if (checkbox.is(':checked')) {
            avenantsForm.show();
            titleForm.show();
        } else {
            avenantsForm.hide();
            titleForm.hide();
        }
    }

    checkbox.on('change', function() {
        toggleElements();
        console.log("changed")
    });
    toggleElements();

    /** hidden & show elements */
    // set visibility for type localisation
    setVisible('#id_immeubles-0-Type_localisation', '#id_immeubles-0-Ville, #id_immeubles-0-pays, #id_immeubles-0-Rue', '1') // 1 - Extérieure
    setVisible('#id_immeubles-0-Type_localisation', '#id_immeubles-0-region,  #id_immeubles-0-departement, #id_immeubles-0-arrondissement, #id_immeubles-0-Quartier', '2') // 2 - National

    // set visibility for type personne
    setVisible('#id_Type_personne', '#id_Nom_prenom, #id_Maticule, #id_Type_id_bailleur, #id_Num_doc, #id_Date_delivrance_doc, #id_Document_identification', '2') // 2 - personne physique
    setVisible('#id_Type_personne', '#id_Raison_social', '1') // 1 - personne morale 

    // toggle occupants visibility 
    toogleFormset("#id_immeubles-0-Type_location", "2", '#occupants_residence-0', '#occupants_bureau-0')
    toogleFormset("#id_immeubles-0-Type_location", "1", '#occupants_bureau-0', '#occupants_residence-0')

    // utils functions for saving collecte 
    function collectAyantsDroits() {
        const result = [];

        $('#ayantdroit-collecte-table tbody tr[data="ayantdroit"]').each(function () {
            const $row = $(this);
            const obj = {
                Nom_Prenom: $row.find('input[name="Nom_Prenom_hidden[]"]').val(),
                Contact: $row.find('input[name="Contact_hidden[]"]').val(),
                Reference_Grosse: $row.find('input[name="Reference_Grosse_hidden[]"]').val(),
                Date_prise_effet_grosse: $row.find('input[name="Date_prise_effet_grosse_hidden[]"]').val(),
                Reference_certificat_non_effet: $row.find('input[name="Reference_certificat_non_effet_hidden[]"]').val(),
                Date_prise_effet_certificat_non_effet: $row.find('input[name="Date_prise_effet_certificat_non_effet_hidden[]"]').val(),
            };

            result.push(obj);
        });

        return result;
    }

    function getNonMandatementData() {
        let data = [];

        $("#nonmandatement-collecte-table tbody tr[data='nonmandatement']").each(function () {
            let row = $(this);

            let exercice = row.find("input[name='Exercice_hidden[]']").val();
            let loyer = row.find("input[name='Loyer_hidden[]']").val();
            let refAttestation = row.find("input[name='Ref_Attestattion_hidden[]']").val();

            // récupération des mois (true/false ou valeur cochée)
            let mois = {
                janvier: row.find("input[name='janvier_hidden[]']").val(),
                fevrier: row.find("input[name='fevrier_hidden[]']").val(),
                mars: row.find("input[name='mars_hidden[]']").val(),
                avril: row.find("input[name='avril_hidden[]']").val(),
                mai: row.find("input[name='mai_hidden[]']").val(),
                juin: row.find("input[name='juin_hidden[]']").val(),
                juillet: row.find("input[name='juillet_hidden[]']").val(),
                aout: row.find("input[name='aout_hidden[]']").val(),
                septembre: row.find("input[name='septembre_hidden[]']").val(),
                octobre: row.find("input[name='octobre_hidden[]']").val(),
                novembre: row.find("input[name='novembre_hidden[]']").val(),
                decembre: row.find("input[name='decembre_hidden[]']").val(),
            };

            let montantTotal = row.find("input[name='Montant_total_hidden[]']").val();
            let visa = row.find("input[name='Visa_hidden[]']").val() === "true";
            console.log("visa value : " ,visa)
            let refContrat = row.find("input[name='Ref_contrat_hidden[]']").val();

            data.push({
                exercice,
                loyer,
                refAttestation,
                mois,
                montantTotal,
                visa,
                refContrat
            });
        });

        return data;
    }

    function collectOccupantsResidence() {
        const result = [];

        $('#occupant-collecte-table tbody tr[data="occupant"]').each(function () {
            const $row = $(this);

            const obj = {
                Nom_Prenom: $row.find('input[name="Nom_Prenom_hidden[]"]').val(),
                Administration_tutelle: $row.find('input[name="Administration_tutelle_hidden[]"]').val(),
                Fonction: $row.find('input[name="Fonction_hidden[]"]').val(),
                Matricule: $row.find('input[name="Matricule_hidden[]"]').val(),
                NIU: $row.find('input[name="NIU_hidden[]"]').val(),
                Ref_ActeJuridique: $row.find('input[name="Ref_ActeJuridique_hidden[]"]').val(),
                Date_Signature_acte_juridique: $row.find('input[name="Date_Signature_acte_juridique_hidden[]"]').val(),
                Telephone: $row.find('input[name="Telephone_hidden[]"]').val(),
            };

            result.push(obj);
        });

        return result;
    }

    function collectOccupantsBureau() {
        const result = [];

        $('#occupantbureau-collecte-table tbody tr[data="occupantbureau"]').each(function () {
            const $row = $(this);

            const obj = {
                Service: $row.find('input[name="Service_hidden[]"]').val(),
                Administration_correspondante: $row.find('input[name="Administration_correspondante_hidden[]"]').val(),
                Fonction: $row.find('input[name="Fonction_hidden[]"]').val(),
                Ref_ActeJuridique_attribution: $row.find('input[name="Ref_ActeJuridique_attribution_hidden[]"]').val(),
                Contact: $row.find('input[name="Contact_hidden[]"]').val(),
                Date_initial_acte_occupation: $row.find('input[name="Date_initial_acte_occupation_hidden[]"]').val(),
            };

            result.push(obj);
        });

        return result;
    }

    function collectPieces() {
        let pieces = [];
        let errors = [];

        $('#pieces-collecte-container .piece-entry').each(function () {
            let pieceId = $(this).data('piece-id');  // chaque div doit avoir data-piece-id
            let libelle = $(this).data('piece-libelle'); // utile pour messages d'erreur
            let statut = $(this).find('input[type=checkbox]').is(':checked');
            let nombre = parseInt($(this).find('input[type=number]').val()) || 0;

            // Validation côté client
            if (statut && nombre <= 0) {
                errors.push(`La pièce « ${libelle} » est cochée mais aucun nombre valide n’a été saisi.`);
            }

            pieces.push({
                piece_id: pieceId,
                statut: statut,
                nombre: nombre
            });
        });

        return {pieces, errors};
    }


    function collectImmeubles() {
        let immeubles = [];
        let errors = [];

        // Chaque immeuble du formset
        $("#immeubles-0").each(function (idx) {
            let immeuble = {};

            // Identification
            immeuble.Designation = $(this).find("[name$='Designation']").val();
            immeuble.Construction = $(this).find("[name$='Construction']").val();
            immeuble.Date_Construction = $(this).find("[name$='Date_Construction']").val();
            immeuble.Nombre_de_pieces = $(this).find("[name$='Nombre_de_pieces']").val();
            immeuble.Superficie_louer = $(this).find("[name$='Superficie_louer']").val();
            immeuble.Norme = $(this).find("[name$='Norme']").val();
            immeuble.Type_location = $(this).find("[name$='Type_location']").val();

            // Localisation
            immeuble.Type_localisation = $(this).find("[name$='Type_localisation']").val();
            immeuble.pays = $(this).find("[name$='pays']").val();
            immeuble.Ville = $(this).find("[name$='Ville']").val();
            immeuble.Rue = $(this).find("[name$='Rue']").val();
            immeuble.region = $(this).find("[name$='region']").val();
            immeuble.departement = $(this).find("[name$='departement']").val();
            immeuble.arrondissement = $(this).find("[name$='arrondissement']").val();
            immeuble.Quartier = $(this).find("[name$='Quartier']").val();
            immeuble.Coordonee_gps = $(this).find("[name$='Coordonee_gps']").val();

            // État physique
            immeuble.Situation_de_la_batisse = $(this).find("[name$='Situation_de_la_batisse']").val();
            immeuble.Revetement_interieure = $(this).find("[name$='Revetement_interieure']").val();
            immeuble.Revetement_exterieure = $(this).find("[name$='Revetement_exterieure']").val();
            immeuble.observation = $(this).find("[name$='observation']").val();

            // Description dynamique (elements)
            let elements = [];
            $(this).find("[name^='immeubles-0-element_']").each(function () {
                let name = $(this).attr("name");
                if (name.endsWith("_statut")) {
                    let id = name.split("_")[1];
                    let statut = $(this).is(":checked");
                    let nombre = parseInt($("[name='immeubles-0-element_" + id + "_nombre']").val()) || 0;

                    // Validation côté client (comme pour les pièces)
                    if (statut && nombre <= 0) {
                        errors.push(`Dans l'immeuble n°${idx + 1}, l’élément #${id} est coché mais aucun nombre valide n’a été saisi.`);
                    }

                    elements.push({
                        element_id: id,
                        statut: statut,
                        nombre: nombre,
                    });
                }
            });
            immeuble.elements = elements;

            immeubles.push(immeuble);
        });

        return { immeubles, errors };
    }

    // process to the data saving : 
    $(document).on("click", "#submit-id-save", function (e) {
        e.preventDefault();
        let formData = new FormData($("#collecte-form")[0]);
        // avenants
        let avenants = [];
        const {pieces, errors: pieceErrors} = collectPieces();
        const ayants_droits = collectAyantsDroits();
        const nonMandatements = getNonMandatementData();
        const occupantsResidences = collectOccupantsResidence();
        const occupantsBureaux = collectOccupantsBureau();
        const {immeubles, errors: immeublesElementsErrors} = collectImmeubles();

        // getting avenant form collecte form
        $('#avenant-collecte-list .avenant-entry').each(function () {
            let data = $(this).data('avenant');
            avenants.push(data); // Chaque data est un objet avenant
        });

        // Validation JS for pieces collectes
        if (pieceErrors.length > 0) {
            showAlertMessage(pieceErrors, '#form-error-collecte');
            return;
        }

        // Validation JS for pieces collectes
        if (immeublesElementsErrors.length > 0) {
            showAlertMessage(immeublesElementsErrors, '#form-error-collecte');
            return;
        }

        console.log(nonMandatements);
        formData.append('pieces_data', JSON.stringify(pieces));
        formData.append('avenants_data', JSON.stringify(avenants));
        formData.append('ayants_droits_data', JSON.stringify(ayants_droits));
        formData.append('nonmandatements_data', JSON.stringify(nonMandatements));
        formData.append('occupantsResidences_data', JSON.stringify(occupantsResidences));
        formData.append('occupantsBureaux_data', JSON.stringify(occupantsBureaux));
        formData.append('immeubles_data', JSON.stringify(immeubles));
        $.ajax({
            url: "/collecte/create",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                showAlertMessage(response.message, '#form-success-collecte')
            },
            error: function (xhr, status, error) {
                let errors = xhr.responseJSON.errors;
                showAlertMessage(errors, '#form-error-collecte')
            }
        });
    });
})