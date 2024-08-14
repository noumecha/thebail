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
  $('#id_Type_personne').on('input', function () {
    var type_personne = $(this).val();
    console.log('type_personne : ', type_personne);
    $('.bailleur_nom_prenom').show();
    $('.bailleur_num_cni').show();
    $('.bailleur_date_deliv_cni').show();
    $('.bailleur_date_creation_ent').show();
    $('.bailleur_raison_social').show();
    $('.bailleur_registre_commerce').show();
    switch (type_personne) {
      case '1':
        $('.bailleur_nom_prenom').hide();
        $('.bailleur_num_cni').hide();
        $('.bailleur_date_deliv_cni').hide();
        $('#id_Registre_commerce').attr('required', true);
        break;
      case '2':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_date_creation_ent').hide();
        $('.bailleur_raison_social').hide();
        $('.bailleur_registre_commerce').hide();
        break;
      case '':
        $('.bailleur_nom_prenom').show();
        $('.bailleur_num_cni').show();
        $('.bailleur_date_deliv_cni').show();
        $('.bailleur_date_creation_ent').show();
        $('.bailleur_raison_social').show();
        $('.bailleur_registre_commerce').show();
        break;
    }
    /*if (type_personne === '1') {
      $('.bailleur_nom_prenom').hide();
      $('.bailleur_num_cni').hide();
      $('.bailleur_date_deliv_cni').hide();
    } else {
      $('.bailleur_nom_prenom').show();
      $('.bailleur_num_cni').show();
      $('.bailleur_date_deliv_cni').show();
      $('.bailleur_date_creation_ent').hide();
      $('.bailleur_raison_social').hide();
      $('.bailleur_registre_commerce').hide();
    }*/
  });
});
