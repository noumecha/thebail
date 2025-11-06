import os
import subprocess
from django.conf import settings

def generate_pdf_from_html(html_path, output_path):
    """Génère un PDF à partir d'un fichier HTML en utilisant la version portable de WeasyPrint."""
    weasyprint_path = os.path.join(settings.BASE_DIR, 'utils', 'weasyprint', 'weasyprint.exe')

    if not os.path.exists(weasyprint_path):
        raise FileNotFoundError("Le binaire portable de WeasyPrint est introuvable.")

    command = [weasyprint_path, html_path, output_path]
    subprocess.run(command, check=True)
