from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from web_project import TemplateLayout
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import models
from django.core.paginator import Paginator

#generic view for basic operation
class BaseCRUDView(TemplateView):
    # model and form
    model = None
    form_class = None
    formset_class = None
    # query and routes
    search_fields = []
    paginate_by = 20
    list_route = None
    fields = []
    filters = []
    delete_url = ""
    # templates
    headers = []
    partial_template = 'layout/partials/crud_table.html'
    list_template = None
    form_template = 'layout/form_template.html'
    # names and objects
    context_object_name = 'objects'
    object_name = None

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context["form"] = self.form_class
        filters_context = []
        for f in self.filters:
            # --- GESTION DES FILTRES ---
            # chaque élément peut être :
            # - un modèle Django (ex: Cellule)
            # - une TextChoices (ex: RoleUtilisateur)
            # - un tuple (nom_du_champ, source)
            # - un iterable [(value, label), ...]
            if isinstance(f, (list, tuple)) and len(f) == 2:
                field_name, source = f
            else:
                source = f
                field_name = getattr(source, "__name__", "filter").lower()
            # 🔹 Cas 1 : modèle Django
            if hasattr(source, "objects"):
                try:
                    items = source.objects.all()
                    # Si le modèle a une date de création, on peut trier
                    if hasattr(source, "Date_creation"):
                        items = items.order_by("-Date_creation")
                    filters_context.append({
                        "name": field_name,
                        "type": "model",
                        "items": items
                    })
                    continue
                except Exception:
                    pass
            # 🔹 Cas 2 : TextChoices
            try:
                if issubclass(source, models.TextChoices):
                    filters_context.append({
                        "name": field_name,
                        "type": "choices",
                        "items": [{"value": c.value, "label": c.label} for c in source]
                    })
                    continue
            except TypeError:
                pass
            # 🔹 Cas 3 : Iterable de tuples (value, label)
            try:
                items = list(source)
                if items and isinstance(items[0], (list, tuple)) and len(items[0]) >= 2:
                    filters_context.append({
                        "name": field_name,
                        "type": "iterable",
                        "items": [{"value": v, "label": l} for v, l in items]
                    })
                    continue
            except Exception:
                pass
        context["filters"] = filters_context
        return context

    def get_queryset(self, search_query=None):
        queryset = self.model.objects.all().order_by('-Date_creation')
        request = getattr(self, 'request', None)
        if not request:
            return queryset
        # 🔍 1. Appliquer les filtres dynamiques (ex: cellule, role, statut, etc.)
        filters = {}
        for key, value in request.GET.items():
            if key in ['search', 'page']:  # on ignore la recherche et la pagination
                continue
            if value:  # ignorer les valeurs vides
                filters[key] = value
        if filters:
            queryset = queryset.filter(**filters)
        # 🔎 2. Appliquer la recherche textuelle si elle existe
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
        return queryset.order_by('-Date_creation')[:100]

    def get_form_view(self, request, pk=None):
        instance = get_object_or_404(self.model, pk=pk) if pk else None
        form = self.form_class(instance=instance)
        formsets = {
            name: formset_class(instance=instance)
            for name, formset_class in getattr(self, "formsets_classes", {}).items()
        }
        html = render_to_string(self.form_template, {
            'form': form,
            "formsets": formsets
        }, request=request)
        return JsonResponse({'success': True, 'html':html})

    def get_list_data(self, request):
        search_query = request.GET.get('search', '').strip()
        queryset = self.get_queryset(search_query)
        paginator = Paginator(queryset, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        html = render_to_string(
            self.partial_template,
            {
                self.context_object_name: page_obj,
                'objects' : page_obj,
                'page_obj': page_obj,
                'paginator': paginator,
                'headers': self.headers,
                'fields': self.fields,
                'delete_url': self.delete_url,
                'object_name': self.object_name or self.model._meta.verbose_name.title(),
            },
            request=request
        )
        return JsonResponse({
            'success': True,
            'html': html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            formsets_valid = True
            for name, formset_class in getattr(self, "formsets_classes", {}).items():
                formset = formset_class(request.POST, instance=obj)
                if formset.is_valid():
                    formset.save()
                else:
                    formsets_valid = False
            if formsets_valid:
                return JsonResponse({
                    'success': True,
                    'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                    'data': {'id': obj.id, 'text': str(obj)}
                })
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                'data': {
                    'id' : obj.id,
                    'text': str(obj)
                }
            })
        # error case
        html = render_to_string(self.form_template, {'form': form}, request=request)
        return JsonResponse({
            'success': False,
            'message': f'Erreur lors de l\'enregistrement',
            'errors' : form.errors,
            'html' : html
        })

    def update(self, request, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return JsonResponse({'success': False, 'message': 'Objet non trouvé'}, status=404)
        instance = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            formsets_valid = True
            for name, formset_class in getattr(self, "formsets_classes", {}).items():
                formset = formset_class(request.POST, instance=obj)
                if formset.is_valid():
                    formset.save()
                else:
                    formsets_valid = False
            if formsets_valid:
                return JsonResponse({
                    'success': True,
                    'message': f'{self.model._meta.verbose_name} enregistré avec succès',
                    'data': {'id': obj.id, 'text': str(obj)}
                })
            return JsonResponse({
                'success' : True,
                'message': f'{self.model._meta.verbose_name} mis à jour avec succès'
            })
        # error case
        html = render_to_string(self.form_template, {'form' : form}, request=request)#, "formset": formset
        return JsonResponse({
            'success' : False,
            'messages': f"Erreur lors de la mise à jour",
            'html' : html
        })

    def delete(self, request, pk):
        try:
            obj = get_object_or_404(self.model, pk=pk)
            obj.delete()
            messages.success(request, f"{self.model._meta.verbose_name} supprimé avec succès!")
            return redirect(self.list_route)
        except obj.DoesNotExist:
            messages.success(request, f"{self.model._meta.verbose_name} non trouvé !")
            return redirect(self.list_route)

    def partial_form_view(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({
                    'success' : True,
                    'id' : obj.id,
                    'text': str(obj)
                })
            html = render_to_string(self.form_template, {'form': form}, request=request)
            return JsonResponse({
                'success': False,
                'html': html
            })
        else:
            form = self.form_class()
            html = render_to_string(self.form_template, {'form': form}, request=request)
            return JsonResponse({'html': html})

    def dispatch(self, request, *args, **kwargs):
        action = kwargs.pop('action', None)
        if action == 'list':
            return self.get_list_data(request)
        elif action == 'form':
            return self.get_form_view(request, kwargs.get('pk'))
        elif action == 'update':
            return self.update(request, **kwargs)
        elif action == 'delete':
            return self.delete(request, kwargs.get('pk'))
        elif action == 'partial_form':
            return self.partial_form_view(request)
        return super().dispatch(request, *args, **kwargs)
