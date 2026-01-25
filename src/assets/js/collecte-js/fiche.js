function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

let index = 0;

document.getElementById('addDocument').addEventListener('click', () => {
  index++;

  document.getElementById('documentsContainer').insertAdjacentHTML(
    'beforeend',
    `
    <div class="card mt-3 p-3 document-item">
      <strong>Document ${index}</strong>

      <input class="form-control mt-2 doc-titre" placeholder="Titre" required>
      <input class="form-control mt-2 doc-type" placeholder="Type" required>
      <input type="file" class="form-control mt-2 doc-file" required>
    </div>
    `
  );
});

document.getElementById('ficheCollecteForm').addEventListener('submit', async e => {
  e.preventDefault();

  const formData = new FormData();
  const apiUrl = document.getElementById('apiUrl').value;

  formData.append('objet', document.getElementById('objet').value);
  formData.append('date_collecte', document.getElementById('date_collecte').value);
  formData.append('statut', 'brouillon');

  formData.append(
    'metadonnees',
    JSON.stringify({
      source: document.getElementById('source').value,
      responsable: document.getElementById('responsable').value
    })
  );

  document.querySelectorAll('.document-item').forEach((doc, i) => {
    formData.append(`documents[${i}][titre]`, doc.querySelector('.doc-titre').value);
    formData.append(`documents[${i}][type_document]`, doc.querySelector('.doc-type').value);
    formData.append(`documents[${i}][fichier]`, doc.querySelector('.doc-file').files[0]);
  });

  const response = await fetch(apiUrl, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  });

  const result = await response.json();

  if (!response.ok) {
    alert(JSON.stringify(result, null, 2));
    return;
  }

  alert('Fiche créée avec succès !');
});
