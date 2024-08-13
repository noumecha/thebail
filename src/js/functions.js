$(document).ready(function () {
  // this is for immeuble
  $('#id_Type_construction').on('input', function () {
    var type_construction = $(this).val();
    console.log('type_construction:', type_construction);
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
});
