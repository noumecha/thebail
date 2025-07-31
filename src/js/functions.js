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
    $('.bailleur_date_creation_ent').show();
    $('.bailleur_raison_social').show();
    $('.bailleur_registre_commerce').show();
    $('#div_id_Type_id_bailleur').show();
    switch (type_personne) {
      case '1':
        $('.bailleur_nom_prenom').hide();
        $('.bailleur_type_id').hide();
        $('#id_Registre_commerce').attr('required', true);
        $('#id_Raison_social').attr('required', true);
        $('#id_Date_creationEnt').attr('required', true);
        $('#div_id_Type_id_bailleur').attr('required', false);
        break;
      case '2':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_date_creation_ent').hide();
        $('.bailleur_raison_social').hide();
        $('.bailleur_registre_commerce').hide();
        $('.bailleur_type_id').show();
        $('#div_id_Type_id_bailleur').attr('required', true);
        $('#id_Nom_prenom').attr('required', true);
        break;
      case '':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_date_creation_ent').show();
        $('.bailleur_raison_social').show();
        $('.bailleur_registre_commerce').show();
        break;
    }
  });
});
