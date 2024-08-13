from django.contrib import admin

from django.contrib.admin import AdminSite
from .models import Contrats,Avenants,Bailleurs,Locataires,Immeubles,Dossiers_Reglements,Occupants,Localisation,Ayant_droits

class EventAdminsite(AdminSite) :
    site_header = 'Baux Admin'
    site_tittle = 'Portail de gestion des baux'
    index_title = ' SGBD du projet "baux administratif"'

event_admin_site =EventAdminsite( name='event_admin')


"""# Register your models here.
admin.site.register(Contrats)
admin.site.register(Bailleurs)
admin.site.register(Locataires)
admin.site.register(Immeubles)
admin.site.register(Dossiers_Reglements)
admin.site.register(Occupants)
admin.site.register(Localisation)
admin.site.register(Ayant_droits)
"""

event_admin_site.register(Contrats)
event_admin_site.register(Bailleurs)
event_admin_site.register(Locataires)
event_admin_site.register(Immeubles)
event_admin_site.register(Dossiers_Reglements)
event_admin_site.register(Occupants)
event_admin_site.register(Localisation)
event_admin_site.register(Ayant_droits)