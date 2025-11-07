from dal import autocomplete
from django.db.models import Q
from ..models import Structures, Administrations, AgentCollecte, Bailleurs, Arrondissemements

# autopcomplete task in partialing form
class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Structures.objects.all()
        # debug utile pendant dev
        print("GET params:", self.request)
        print("forwarded:", getattr(self, 'forwarded', None))
        # 1) Valeur forwardée par DAL
        administration_val = None
        if hasattr(self, 'forwarded'):
            administration_val = self.forwarded.get('Administration_correspondante')
        # 2) Autres formes possibles (au cas où)
        if not administration_val:
            administration_val = self.request.GET.get('administration_id') or self.request.GET.get('forward[Administration_correspondante]')
        if administration_val:
            # éventuellement caster en int si nécessaire
            try:
                administration_val = int(administration_val)
                qs = qs.filter(Administration_id=administration_val)
            except (ValueError, TypeError):
                # cas où forwarded donne une chaîne (par ex. label) : essayer filtre par nom si besoin
                qs = qs.filter(Administration__Nom__icontains=str(administration_val))
        if self.q:
            qs = qs.filter(LibelleFr__icontains=self.q)
        return qs

class StructureAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Structures.objects.all()
        if self.q:
            qs = qs.filter(LibelleFr__icontains=self.q)
        return qs

class AdminAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Administrations.objects.all()
        if self.q:
            qs = qs.filter(LibelleFr__icontains=self.q)
        return qs

class AgentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AgentCollecte.objects.all()
        if self.q:
            qs = qs.filter(
                Q(Matricule__icontains=self.q)
            )
        return qs

class BailleurAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Bailleurs.objects.all()
        if self.q:
            qs = qs.filter(
                Q(Nom_prenom__icontains=self.q) | Q(Raison_social__icontains=self.q)
            )
        return qs

class ArrondissementAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Arrondissemements.objects.all().order_by('AbreviationFr')
        if self.q:
            qs = qs.filter(
                Q(LibelleFR__icontains=self.q) | Q(AbreviationFr__icontains=self.q)
            )
        return qs
