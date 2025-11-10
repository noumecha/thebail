from django import template
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
import re
from django.template.loader import render_to_string
register = template.Library()

@register.filter
def crispy_variant(field, variant="default"):
    """
    Rendu d'un champ crispy avec un variant visuel.
    Exemples de variant : 'no_label', 'inline_label', 'left_label', 'default'
    """
    html = render_to_string(as_crispy_field(field))

    # selon le variant choisi, tu modifies ou entoures le HTML rendu
    if variant == "no_label":
        # on supprime le label s’il est inclus
        html = re.sub(r'<label[^>]*>.*?</label>', '', html, flags=re.DOTALL)

    elif variant == "inline_label":
        # Label à l’intérieur du champ (exemple simplifié)
        html = f"""
        <div class="form-floating">
            {html}
            <label for="{field.id_for_label}">{field.label}</label>
        </div>
        """

    elif variant == "left_label":
        # label à gauche suivi du champ, séparé par ":"
        html = f"""
        <div class="d-flex align-items-center gap-2">
            <label for="{field.id_for_label}" class="fw-bold">{field.label} :</label>
            <div class="flex-grow-1">{as_crispy_field(field)}</div>
        </div>
        """

    return html
