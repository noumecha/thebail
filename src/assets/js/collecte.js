$(function () {
    // set visibility on modal load initialization
    setVisible('id_immeubles-0-Type_localisation', '#id_Ville, #id_Rue', '1') // 1 - Extérieure
    setVisible('id_immeubles-0-Type_localisation', '#id_region, #id_departement, #id_arrondissement, #id_Quartier', '2') // 2 - National

    // toggle occupants visibility 
    toogleFormset("#id_Type_location", "2", '#batiment_occ_residence-0', '#batiment_occ_bureaux-0')
    toogleFormset("#id_Type_location", "1", '#batiment_occ_bureaux-0', '#batiment_occ_residence-0')
})