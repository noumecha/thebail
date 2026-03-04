from django.http import JsonResponse
from django.apps import apps
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def add_dynamic_choice(request):
    if request.method == 'GET':
        return JsonResponse({"message": "cette url n'accepte que la méthode POST."}, status=200)

    # POST logic...
    model_name = request.POST.get("model")
    label = request.POST.get("label", "").strip()

    if not model_name or not label:
        return JsonResponse({"error": "Données invalides."}, status=400)

    Model = apps.get_model("baux", model_name)
    if Model.objects.filter(libelle__iexact=label).exists():
        return JsonResponse({
            "error": "Ce libellé existe déjà."
        }, status=409)

    obj = Model.objects.create(libelle=label)

    return JsonResponse({
        "id": obj.pk,
        "label": obj.libelle,
        "created": True
    })
