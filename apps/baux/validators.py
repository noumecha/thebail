from django.core.exceptions import ValidationError

# RIB validator
def rib_validator(value):
    from apps.baux.models import Banques
    rib_prefix = value[:5]
    if not Banques.objects.filter(codeBanque=rib_prefix).exists():
        raise ValidationError("Le code banque du RIB n'est pas valide.")