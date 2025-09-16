$(function () {
    let avenantIndex = 1; // Pour numéroter les avenants
    // objet pour la sauvegarde globale en base de données ---> creer un Array d'objet avenant à soumettre via ajax
    const Avenant = {
        ref: '',
        ancienBailleur: '',
        nouveauBailleur: '',
        montantAncien: '',
        montantNouveau: '',
        attestationAncien: '',
        attestationNouveau: '',
        dureeAncien: '',
        dureeNouveau: '',
        dateSignature: '',
        dateEffet: '',
        modificationApportee: '',
        localite: '',
    }


    $('#avenant-collecte-add-btn').click(function () {
        const ref = $('#id_avenants-0-Ref_Avenant').val();
        const ancienBailleur = $('#id_avenants-0-Ancien_bailleur option:selected').text();
        const nouveauBailleur = $('#id_avenants-0-Nouveau_bailleur option:selected').text();
        const montantAncien = $('#id_avenants-0-Montant_TTC_Mensuel_ancien').val();
        const montantNouveau = $('#id_avenants-0-Montant_TTC_Mensuel_Nouveau').val();
        const attestationAncien = $('#id_avenants-0-Attestion_domicilliation_bancaire_ancien').val();
        const attestationNouveau = $('#id_avenants-0-Attestion_domicilliation_bancaire_nouveau').val();
        const dureeAncien = $('#id_avenants-0-Duree_Contrat_Ancien').val();
        const dureeNouveau = $('#id_avenants-0-Duree_Contrat_Nouveau').val();
        const dateSignature = $('#id_avenants-0-Date_Signature').val();
        const dateEffet = $('#id_avenants-0-Date_effet').val();
        const modificationApportee = $('#id_avenants-0-Modification_apportee').val();
        const localite = $('#id_avenants-0-Localite').val();

        // Validation minimum
        if (!ref) {
            alert("Veuillez renseigner la Référence de l’avenant.");
            return;
        }

        // Cloner le template
        const $entry = $('#avenant-template .avenant-entry').clone();

        // Remplir les champs du tableau
        $entry.find('.ref-avenant').text(avenantIndex.toString().padStart(2, '0'));
        $entry.find('.ancien-bailleur').text(ancienBailleur);
        $entry.find('.nouveau-bailleur').text(nouveauBailleur);
        $entry.find('.ancien-montant').text(montantAncien);
        $entry.find('.nouveau-montant').text(montantNouveau);
        $entry.find('.ancien-attestation').text(attestationAncien);
        $entry.find('.nouveau-attestation').text(attestationNouveau);
        $entry.find('.ancien-duree').text(dureeAncien);
        $entry.find('.nouveau-duree').text(dureeNouveau);

        // Stocker les données dans un attribut data
        $entry.data('avenant', {
            ref, ancienBailleur, nouveauBailleur,
            montantAncien, montantNouveau,
            attestationAncien, attestationNouveau,
            dureeAncien, dureeNouveau, dateSignature, dateEffet,
            modificationApportee, localite
        });

        // Ajouter au DOM
        $('#avenant-collecte-list').append($entry);
        avenantIndex++;

        // Réinitialiser le formulaire (juste le formset à index 0)
        $('#id_avenants-0-Ref_Avenant').val('');
        $('#id_avenants-0-Ancien_bailleur').val('').trigger('change');
        $('#id_avenants-0-Nouveau_bailleur').val('').trigger('change');
        $('#id_avenants-0-Montant_TTC_Mensuel_ancien').val('');
        $('#id_avenants-0-Montant_TTC_Mensuel_Nouveau').val('');
        $('#id_avenants-0-Attestion_domicilliation_bancaire_ancien').val('');
        $('#id_avenants-0-Attestion_domicilliation_bancaire_nouveau').val('');
        $('#id_avenants-0-Duree_Contrat_Ancien').val('');
        $('#id_avenants-0-Duree_Contrat_Nouveau').val('');
        $('#id_avenants-0-Date_Signature').val('');
        $('#id_avenants-0-Date_effet').val('');
        $('#id_avenants-0-Modification_apportee').val('');
        $('#id_avenants-0-Localite').val('');
    });

    // Supprimer un tableau
    $(document).on('click', '.btn-delete', function () {
        if (confirm("Supprimer cet avenant ?")) {
            $(this).closest('.avenant-entry').remove();
        }
    });

    // Éditer un tableau
    $(document).on('click', '.btn-edit', function () {
        const $entry = $(this).closest('.avenant-entry');
        const data = $entry.data('avenant');

        // Remplir le formulaire
        $('#id_avenants-0-Ref_Avenant').val(data.ref);
        $('#id_avenants-0-Ancien_bailleur').val(data.ancienBailleur).trigger('change');
        $('#id_avenants-0-Nouveau_bailleur').val(data.nouveauBailleur).trigger('change');
        $('#id_avenants-0-Montant_TTC_Mensuel_ancien').val(data.montantAncien);
        $('#id_avenants-0-Montant_TTC_Mensuel_Nouveau').val(data.montantNouveau);
        $('#id_avenants-0-Attestion_domicilliation_bancaire_ancien').val(data.attestationAncien);
        $('#id_avenants-0-Attestion_domicilliation_bancaire_nouveau').val(data.attestationNouveau);
        $('#id_avenants-0-Duree_Contrat_Ancien').val(data.dureeAncien);
        $('#id_avenants-0-Duree_Contrat_Nouveau').val(data.dureeNouveau);

        // Supprimer l’entrée actuelle
        $entry.remove();
    });
});
