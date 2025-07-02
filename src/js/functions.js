// this code is for deactivate some fields depending on some conditions
$(document).ready(function () {
  // this is for immeuble
  $('#id_Type_construction').on('input', function () {
    var type_construction = $(this).val();
    console.log('type_construction :', type_construction);
    if (type_construction === 'VILLA') {
      $('#id_Nombre_d_etage').val('1');
    } else {
      $('#id_Nombre_d_etage').val('');
    }
  });
  $('.color_class').hide(); // hide the color input by default
  $('#id_Type_mur').on('input', function () {
    var type_mur = $(this).val();
    console.log('type_mur:', type_mur);
    if (type_mur === 'Peint') {
      $('.color_class').show();
    } else {
      $('.color_class').hide();
    }
  });
  // bailleur
  $(document).on('input', '#id_Type_personne', function () {
    var type_personne = $(this).val();
    console.log('type_personne:', type_personne);
    $('.bailleur_nom_prenom').show();
    $('.bailleur_num_cni').show();
    $('.bailleur_date_deliv_cni').show();
    $('.bailleur_date_creation_ent').show();
    $('.bailleur_raison_social').show();
    $('.bailleur_registre_commerce').show();
    $('#div_id_Type_id_bailleur').show();
    switch (type_personne) {
      case '1':
        $('.bailleur_nom_prenom').hide();
        $('.bailleur_num_cni').hide();
        $('.bailleur_date_deliv_cni').hide();
        $('.bailleur_num_passeport').hide();
        $('.bailleur_date_deliv_passeport').hide();
        $('.bailleur_type_id').hide();
        $('#id_Registre_commerce').attr('required', true);
        $('#id_Reference_doc_identification').attr('required', true);
        $('#id_Raison_social').attr('required', true);
        $('#id_Date_creationEnt').attr('required', true);
        $('#div_id_Type_id_bailleur').attr('required', false);
        $('#id_NIU').attr('required', true);
        break;
      case '2':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_num_passeport').show();
        $('.bailleur_date_deliv_passeport').show();
        $('.bailleur_date_creation_ent').hide();
        $('.bailleur_raison_social').hide();
        $('.bailleur_registre_commerce').hide();
        $('.bailleur_type_id').show();
        $('#div_id_Type_id_bailleur').attr('required', true);
        $('#id_Reference_doc_identification').attr('required', true);
        $('#id_Nom_prenom').attr('required', true);
        $('#id_Num_Cni').attr('required', true);
        $('#id_Date_delivrance_cni').attr('required', true);
        $('#id_NIU').attr('required', true);
        break;
      case '':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_num_passeport').show();
        $('.bailleur_date_deliv_passeport').show();
        $('.bailleur_date_creation_ent').show();
        $('.bailleur_raison_social').show();
        $('.bailleur_registre_commerce').show();
        break;
    }
  });
  // bailleur change identification type (CNI or PASSEPORT)
  $(document).on('input', '#id_Type_id_bailleur', function () {
    var type_id_bailleur = $(this).val();
    console.log('type_id_bailleur:', type_id_bailleur);
    $('.bailleur_num_cni').hide();
    $('.bailleur_date_deliv_cni').hide();
    $('.bailleur_num_passeport').hide();
    $('.bailleur_date_deliv_passeport').hide();
    switch (type_id_bailleur) {
      case 'CNI':
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_num_passeport').hide();
        $('.bailleur_date_deliv_passeport').hide();
        $('#id_Num_Cni').attr('required', true);
        $('#id_Date_delivrance_cni').attr('required', true);
        break;
      case 'PASSEPORT':
        $('.bailleur_num_cni').hide();
        $('.bailleur_date_deliv_cni').hide();
        $('.bailleur_num_passeport').show();
        $('.bailleur_date_deliv_passeport').show();
        $('#id_Num_Cni').attr('required', false);
        $('#id_Date_delivrance_cni').attr('required', false);
        $('#id_NumPassePort').attr('required', true);
        $('#id_Date_delivrance_PassePort').attr('required', true);
        break;
      case '':
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_num_passeport').show();
        $('.bailleur_date_deliv_passeport').show();
        break;
    }
  });
  // representant change identification type (CNI or PASSEPORT)
  $('#id_Type_id_representant').on('input', function () {
    var type_id_bailleur = $(this).val();
    console.log('type_id_representant:', type_id_bailleur);
    $('.representant_num_cni').hide();
    $('.representant_date_deliv_cni').hide();
    $('.representant_num_passeport').hide();
    $('.representant_date_deliv_passeport').hide();
    switch (type_id_bailleur) {
      case 'CNI':
        $('.representant_num_cni').show();
        $('.representant_date_deliv_cni').show();
        $('.representant_num_passeport').hide();
        $('.representant_date_deliv_passeport').hide();
        $('#id_Num_Cni_representant').attr('required', true);
        $('#id_Date_delivrance_cni_representant').attr('required', true);
        break;
      case 'PASSEPORT':
        $('.representant_num_cni').hide();
        $('.representant_date_deliv_cni').hide();
        $('.representant_num_passeport').show();
        $('.representant_date_deliv_passeport').show();
        $('#id_Num_Cni_representant').attr('required', false);
        $('#id_Date_delivrance_cni_representant').attr('required', false);
        $('#id_NumPassePort_representant').attr('required', true);
        $('#id_Date_delivrance_PassePort_representant').attr('required', true);
        break;
      case '':
        $('.representant_num_cni').show();
        $('.representant_date_deliv_cni').show();
        $('.representant_num_passeport').show();
        $('.representant_date_deliv_passeport').show();
        $('#id_Num_Cni_representant').attr('required', false);
        $('#id_Date_delivrance_cni_representant').attr('required', false);
        $('#id_NumPassePort_representant').attr('required', false);
        $('#id_Date_delivrance_PassePort_representant').attr('required', false);
        break;
    }
  });
});
