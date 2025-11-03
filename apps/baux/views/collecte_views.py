from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from web_project import TemplateLayout
from django.template.loader import render_to_string
from ..models import *
from ..forms import *
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
import traceback
import sys
from django.contrib import messages
from weasyprint import HTML, CSS
import os
from django.conf import settings
import qrcode
import base64
from io import BytesIO

# check if instace exist
def instanceExist(model, idEl, msg):
    instance = None
    if idEl == None:
        return JsonResponse({"success": False, "errors": "l'élément selectionné n'exite pas"}, status=400)
    else:
        instance = get_object_or_404(model, pk=idEl)
    #
    if instance:
        return instance
    else:
        return JsonResponse({"success": False, "errors": msg}, status=400)

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def generate_qr_code(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# collecte view
class CollecteView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["collecteList"] = Collectes.objects.all().order_by('-Date_creation')
        pieces = Pieces.objects.all()
        elements = ElementDeDescription.objects.all()
        pk = kwargs.get('pk', None)
        if pk:
            collecte = get_object_or_404(Collectes, pk=pk)
            form = CollectesForm(instance=collecte)
        else:
            form = CollectesForm()
        context['avenants_formset'] = AvenantsFormSet(prefix="avenants")
        context['immeubles_formset'] = ImmeublesFormSet(prefix="immeubles")
        context['ayants_droits_formset'] = AyantDroitsFormSet(prefix="ayants_droits")
        context['occupants_residence_formset'] = OccupantsFormSet(prefix="occupants_residence")
        context['occupants_bureau_formset'] = OccupantBureauxFormSet(prefix="occupants_bureau")
        context['non_mandatements_formset'] = NonMandatementFormSet(prefix="non_mandatements")
        context["form"] = form
        context["pieces"] = pieces
        context["elements"] = elements
        context["is_update"] = pk is not None
        return context

    def print(request, pk):
        # fetch content from db and load template context
        collecte = get_object_or_404(Collectes, pk=pk)
        context = {"collecte" : collecte}
        html = render_to_string("baux/docs/contrat_doc.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="fiche_collecte_{collecte.Numero_fiche_de_collecte}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response

    def printfiche(request, pk):
        collecte = get_object_or_404(Collectes, pk=pk)
        immeuble = Immeubles.objects.filter(Collecte=collecte).first()
        typeconstructions = TypeConstructions.objects.all()
        typelocations = TYPE_LOCATION
        situationbatisses = STATUT_BATISSE
        revetints = RevetementInts.objects.all()
        revetexts = RevetementExts.objects.all()
        # elements in immeuble
        elements = list(ElementDeDescription.objects.all().order_by('id'))
        immeubleelements_qs = ImmeubleElement.objects.filter(immeuble=immeuble)
        immeuble_elements_map = {imel.element_id: imel for imel in immeubleelements_qs}
        element_groups = list(chunk_list(elements, 9))
        # occupants
        occresisendes = Occupants.objects.filter(Immeuble=immeuble)
        occbureaux = OccupantBureaux.objects.filter(Immeuble=immeuble)
        #
        typologiescontrats = TypeContrats.objects.all()
        #
        periodicitereglements = PERIODICITE_LOYER
        # avenant
        avenants = Avenants.objects.filter(collecte=collecte)[:2]
        # bailleurs
        bailleur = collecte.Bailleur
        typepersonnes = TYPE_PERSONNE
        statutsbailleur = STATUT_BAILLEUR
        ayantdroits = Ayant_droits.objects.filter(Bailleur=bailleur)
        nommandatements = Non_Mandatement.objects.filter(Bailleur=bailleur)
        # pieces on collecte
        pieces = list(Pieces.objects.all().order_by('id'))
        pieceselements_qs = PieceCollectes.objects.filter(Collecte_id=collecte.pk)
        pieces_map = {el.Piece_id: el for el in pieceselements_qs}
        pieces_groups = list(chunk_list(pieces, 4))
        # qr code
        qr_data = f"Fiche collecte n° {collecte.Numero_fiche_de_collecte}"  # or a URL
        qr_code_img = generate_qr_code(qr_data)
        # context
        context = {
            "collecte" : collecte,
            "immeuble" : immeuble,
            "typeconstructions" : typeconstructions,
            "typelocations" : typelocations,
            "situationbatisses" : situationbatisses,
            "revetints" : revetints,
            "revetexts" : revetexts,
            "elements_groups": element_groups,
            "immeuble_elements_map": immeuble_elements_map,
            "occresisendes" : occresisendes,
            "occbureaux" : occbureaux,
            "typologiescontrats" : typologiescontrats,
            "periodicitereglements" : periodicitereglements,
            "avenants" : avenants,
            "bailleur" : bailleur,
            "typersonnes" : typepersonnes,
            "statutsbailleur" : statutsbailleur,
            "ayantdroits" : ayantdroits,
            "nommandatements" : nommandatements,
            "pieces_groups" : pieces_groups,
            "pieces_map" : pieces_map,
            # for styles
            "base_url": request.build_absolute_uri("/").rstrip('/'),
            "now": timezone.now(),
            "qr_code_img" : qr_code_img
        }
        html = render_to_string("baux/docs/fiche_doc.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="fiche_collecte_{collecte.Numero_fiche_de_collecte}.pdf"'
        css_files = [
            CSS(filename=os.path.join(settings.STATIC_ROOT, 'css/bootstrap.min.css')),
            CSS(filename=os.path.join(settings.STATIC_ROOT, 'css/style.css')),
        ]
        HTML(string=html).write_pdf(response, stylesheets=css_files)
        return response


class CollecteDeleteView(DeleteView):
    model = Collectes
    template_name = 'baux/collecte_delete.html'
    success_url = reverse_lazy('baux:collecte_list')

    def delete(self, request, *args, **kwargs):
        # récupère l'objet avant suppression
        self.object = self.get_object()
        messages.success(request, f"La fiche de collecte N° {self.object.Numero_fiche_de_collecte} a bien été supprimée !")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = CollectesForm()
        return context

@csrf_exempt
def collecte_create(request):
    if request.method == "POST":
        collecte_form = CollectesForm(request.POST, request.FILES)

        if collecte_form.is_valid():
            #collecte = collecte_form.save()
            try:
                with transaction.atomic():
                    collecte = collecte_form.save()
                    bailleurInstance = get_object_or_404(Bailleurs, pk=collecte.Bailleur.pk)
                    # Sauvegarde des immeubles
                    immeubles_json = request.POST.get("immeubles_data")
                    if immeubles_json:
                        try:
                            immeubles_data = json.loads(immeubles_json)
                            # immeuble validation :
                            errors = []  # pour collecter toutes les errors
                            immeubles_valides = []

                            for idx, im in enumerate(immeubles_data):
                                designation = im.get("Designation")
                                construction = im.get("Construction")

                                # --- Vérification des champs requis ---
                                if not designation:
                                    errors.append(f"Immeuble {idx+1}: 'Designation' est requis.")
                                if not construction:
                                    errors.append(f"Immeuble {idx+1}: 'Type de Construction' est requis.")

                                # --- Vérification des doublons (par exemple même Designation + Ville) ---
                                if designation and Immeubles.objects.filter(
                                    Designation=designation,
                                    Ville=im.get("Ville")
                                ).exists():
                                    errors.append(
                                        f"Immeuble {idx+1} {designation}: déjà existant (Designation + Ville)."
                                    )

                                immeubles_valides.append(im)

                            # S'il y a des errors, on arrête et on retourne la réponse
                            if errors:
                                return JsonResponse({"success": False, "errors": errors}, status=400)

                            for im in immeubles_valides:
                                # getting proper instance base on id
                                typeconstruction = instanceExist(TypeConstructions, im.get("Construction"), "Type de Construction non existant")
                                norme = instanceExist(Normes, im.get("Norme"), "La norme cadastrale selectionné n'existe pas")
                                revInt = instanceExist(RevetementInts, im.get("Revetement_interieure"), "La revetement intérieure selectionné n'existe pas")
                                revExt = instanceExist(RevetementExts, im.get("Revetement_exterieure"), "La revetement extérieure selectionné n'existe pas")
                                region = instanceExist(Regions, im.get("region"), "La région selectionnée n'existe pas")
                                departement = instanceExist(Departements, im.get("departement"), "Le département selectionné n'existe pas")
                                arrondissement = instanceExist(Arrondissemements, im.get("arrondissement"), "L'arrondissemnt selectionnée n'existe pas")
                                #
                                immeuble = Immeubles.objects.create(
                                    Collecte=collecte,
                                    Designation=im.get("Designation"),
                                    Construction=typeconstruction,
                                    Date_Construction=im.get("Date_Construction"),
                                    Nombre_de_pieces=im.get("Nombre_de_pieces"),
                                    Superficie_louer=im.get("Superficie_louer"),
                                    Norme=norme,
                                    Type_location=im.get("Type_location"),
                                    Type_localisation=im.get("Type_localisation"),
                                    pays=im.get("pays"),
                                    Ville=im.get("Ville"),
                                    Rue=im.get("Rue"),
                                    region=region,
                                    departement=departement,
                                    arrondissement=arrondissement,
                                    Quartier=im.get("Quartier"),
                                    Coordonee_gps=im.get("Coordonee_gps"),
                                    Situation_de_la_batisse=im.get("Situation_de_la_batisse"),
                                    Revetement_interieure=revInt,
                                    Revetement_exterieure=revExt,
                                    observation=im.get("observation"),
                                )
                                # Récupération des fichiers envoyés
                                files = request.FILES.getlist("immeuble_images")
                                for f in files:
                                    ImmeubleImage.objects.create(immeuble=immeuble, image=f)

                                # éléments dynamiques liés à l’immeuble
                                for el in im.get("elements", []):
                                    ImmeubleElement.objects.create(
                                        immeuble=immeuble,
                                        element_id=el.get("element_id"),
                                        statut=el.get("statut", False),
                                        nombre=el.get("nombre", 0),
                                    )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des immeubles."}, status=400)

                    # Traitement des ayants droits
                    ayants_droits_json = request.POST.get('ayants_droits_data')
                    if ayants_droits_json:
                        try:
                            ayants_droits = json.loads(ayants_droits_json)

                            for ad in ayants_droits:
                                Ayant_droits.objects.create(
                                    Bailleur=collecte.Bailleur,
                                    Bailleur_id=collecte.Bailleur.pk,
                                    Nom_Prenom=ad.get('Nom_Prenom'),
                                    Contact=ad.get('Contact'),
                                    Reference_Grosse=ad.get('Reference_Grosse'),
                                    Date_prise_effet_grosse=ad.get('Date_prise_effet_grosse'),
                                    Reference_certificat_non_effet=ad.get('Reference_certificat_non_effet'),
                                    Date_prise_effet_certificat_non_effet=ad.get('Date_prise_effet_certificat_non_effet')
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des ayants droits."}, status=400)

                    # Traitement des avenants (données JSON depuis JS)
                    avenants_json = request.POST.get('avenants_data')
                    if avenants_json:
                        try:
                            avenants = json.loads(avenants_json)
                            for a in avenants:
                                # getting proper instance base on id
                                ancienbailleur = instanceExist(Bailleurs, a.get('ancienBailleur'), "Ancien Bailleur selectionné non existant")
                                nouveaubailleur = instanceExist(Bailleurs, a.get('nouveauBailleur'), "Nouveau Bailleur selectionné non existant")
                                # Récupérer le fichier associé si présent
                                file_field_name = f"fichier_avenant_{a.get('ref')}"
                                fichier_avenant = request.FILES.get(file_field_name)
                                #
                                Avenants.objects.create(
                                    collecte=collecte,
                                    Ref_Avenant=a.get('ref'),
                                    Date_Signature=a.get('dateSignature'),
                                    Date_effet=a.get('dateEffet'),
                                    Modification_apportee=a.get('modificationApportee'),
                                    Ancien_bailleur=ancienbailleur,
                                    Nouveau_bailleur=nouveaubailleur,
                                    #Localite=a.get('localite'),
                                    Montant_TTC_Mensuel_ancien=a.get('montantAncien'),
                                    Montant_TTC_Mensuel_Nouveau=a.get('montantNouveau'),
                                    #Attestion_domicilliation_bancaire_ancien=a.get('attestationAncien'),
                                    Attestion_domicilliation_bancaire_nouveau=a.get('attestationNouveau'),
                                    Duree_Contrat_Ancien=a.get('dureeAncien'),
                                    Duree_Contrat_Nouveau=a.get('dureeNouveau'),
                                    Fichier_avenant=fichier_avenant  # ⚡ Le fichier unique
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des avenants."}, status=400)

                    # traitement des nonmandatement
                    nonmandatements_json = request.POST.get('nonmandatements_data')
                    if nonmandatements_json:
                        try:
                            nonmandatements = json.loads(nonmandatements_json)
                            for n in nonmandatements:
                                # getting proper instance base on id
                                exercice = instanceExist(Exercice, n.get('exercice'), "Exercice selectionné non existant")
                                #
                                mois = n.get('mois', {})
                                # gestion du fichier
                                uid = n.get("uid")
                                fichier = request.FILES.get(f"nonmandatement_file_{uid}")
                                #
                                Non_Mandatement.objects.create(
                                    Exercice=exercice,
                                    Loyer_Mensuel=n.get('loyer'),#Loyer_Mensuel
                                    Ref_Attestattion=n.get('refAttestation'),#Ref_Attestattion
                                    Date_Signature=n.get('dateSignature'),
                                    janvier=mois.get('janvier'),
                                    fevrier=mois.get('fevrier'),
                                    mars=mois.get('mars'),
                                    avril=mois.get('avril'),
                                    mai=mois.get('mai'),
                                    juin=mois.get('juin'),
                                    juillet=mois.get('juillet'),
                                    aout=mois.get('aout'),
                                    septembre=mois.get('septembre'),
                                    octobre=mois.get('octobre'),
                                    novembre=mois.get('novembre'),
                                    decembre=mois.get('decembre'),
                                    Montant_total_exercice=n.get('montantTotal'),#Montant_total_exercice
                                    Visa_budgétaire=n.get('visa'),
                                    Ref_contrat_avenant=n.get('refContrat'),#Ref_contrat_avenant
                                    Bailleur=collecte.Bailleur,
                                    Bailleur_id=collecte.Bailleur.pk,
                                    Fichier_nonmandatement=fichier if fichier else None
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des attestation de non mandatement."}, status=400)

                    # traitement des occupants
                    # residence
                    occupantsResidences_json = request.POST.get('occupantsResidences_data')
                    if occupantsResidences_json:
                        try:
                            occupantsResidences = json.loads(occupantsResidences_json)

                            for obj in occupantsResidences:
                                # getting proper instance base on id
                                tutelle = instanceExist(Administrations, obj.get('Administration_tutelle'), "Administration tutelle selectionné non existant")
                                #
                                Occupants.objects.create(
                                    Nom_Prenom = obj.get('Nom_Prenom'),
                                    Administration_tutelle = tutelle,
                                    Fonction = obj.get('Fonction'),
                                    Matricule = obj.get('Matricule'),
                                    NIU = obj.get('NIU'),
                                    Ref_ActeJuridique = obj.get('Ref_ActeJuridique'),
                                    Date_Signature_acte_juridique = obj.get('Date_Signature_acte_juridique'),
                                    Telephone = obj.get('Telephone'),
                                    Immeuble=immeuble,
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des occupants résidents."}, status=400)

                    # bureau
                    occupantsBureaux_json = request.POST.get('occupantsBureaux_data')
                    if occupantsBureaux_json:
                        try:
                            occupantsBureaux = json.loads(occupantsBureaux_json)

                            for obj in occupantsBureaux:
                                # getting proper instance base on id
                                service = instanceExist(Structures, obj.get('Service'), "Service selectionné non existant")
                                administration = instanceExist(Administrations, obj.get('Administration_correspondante'), "Administration correspondante selectionnée non existant")
                                #
                                OccupantBureaux.objects.create(
                                    Service=service,
                                    Administration_correspondante=administration,
                                    Fonction=obj.get('Fonction'),
                                    Ref_ActeJuridique_attribution=obj.get('Ref_ActeJuridique_attribution'),
                                    Contact=obj.get('Contact'),
                                    Date_initial_acte_occupation=obj.get('Date_initial_acte_occupation'),
                                    Immeuble=immeuble,
                                )
                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des occupants de bureaux"}, status=400)

                    # traitement des pièces collectés
                    pieces_json = request.POST.get('pieces_data')
                    if pieces_json:
                        try:
                            pieces_data = json.loads(pieces_json)
                            for p in pieces_data:
                                piece_id = p.get('piece_id')
                                statut = p.get('statut', False)
                                nombre = p.get('nombre', 0)

                                # Validation côté serveur (sécurité)
                                if statut and (not nombre or nombre <= 0):
                                    return JsonResponse({
                                        "success": False,
                                        "errors": f"La pièce {piece_id} est cochée mais sans nombre valide."
                                    }, status=400)

                                if statut or nombre > 0:
                                    PieceCollectes.objects.create(
                                        Collecte=collecte,
                                        Piece_id=piece_id,
                                        statut=statut,
                                        nombre=nombre
                                    )

                        except json.JSONDecodeError:
                            return JsonResponse({"success": False, "errors": "Erreur lors du décodage des pièces collectées."}, status=400)

                    return JsonResponse({"success": True, "message": "Fiche de collecte enregistrée avec succès !"})
            except Exception as e:
                # rollback automatique si exception
                exc_type, exc_obj, exc_tb = sys.exc_info()
                ligne = exc_tb.tb_lineno  # récupère le numéro de ligne exact
                erreur_complete = traceback.format_exc()  # stacktrace complet
                return JsonResponse({
                    "success": False,
                    "errors": str(e),
                    "line": ligne,
                    "trace": erreur_complete
                }, status=400)
        else:
            return JsonResponse({"success": False, "errors": collecte_form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)
