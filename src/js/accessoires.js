document.addEventListener('DOMContentLoaded', function () {
  const accessoiresList = document.getElementById('accessoires-list');
  const accessoiresDataInput = document.getElementById('accessoire_data');
  const addAccessoireButton = document.getElementById('add-accessoire');

  addAccessoireButton.addEventListener('click', function () {
    const libelle = document.querySelector('input[name="libelle"]').value;
    const quantite = document.querySelector('input[name="quantite"]').value;

    if (libelle && quantite) {
      const li = document.createElement('li');
      li.textContent = `${libelle} - Quantité : ${quantite}`;
      accessoiresList.appendChild(li);

      let currentData = accessoiresDataInput.value;
      currentData += `${libelle}:${quantite};`;
      accessoiresDataInput.value = currentData;

      // Effacer les entrées après l'ajout
      document.querySelector('input[name="libelle"]').value = '';
      document.querySelector('input[name="quantite"]').value = '';
    }
  });
});
