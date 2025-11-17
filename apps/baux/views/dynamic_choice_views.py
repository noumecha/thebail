from django.http import JsonResponse
from django.apps import apps
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def add_dynamic_choice(request):
    if request.method == 'GET':
        return JsonResponse({"message": "cette url n'accepte que la méthode POST."}, status=200)

    # POST logic...
    model_name = request.POST.get("model")
    label = request.POST.get("label", "").strip()

    if not model_name or not label:
        return JsonResponse({"error": "Invalid data"}, status=400)

    # Dynamically load the model by its name
    Model = apps.get_model("baux", model_name)

    obj, created = Model.objects.get_or_create(libelle=label)

    return JsonResponse({
        "id": obj.pk,
        "label": obj.libelle,
        "created": created
    })
