from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from ..models import Locataires, Recensements
from ..forms import RecensementsForm
from web_project import TemplateLayout

#generic view for basic operation
class BaseCRUDView(TemplateView):
    model = None
    form_class = None
    formset_class = None
    list_template = None
    list_route = None
    partial_template = None
    form_template = 'baux/partials/form_template.html'
    context_object_name = 'objects'
    search_fields = []
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context[self.context_object_name] = self.model.objects.all()
        context["form"] = self.form_class
        return context

    def get_queryset(self, search_query=None):
        queryset = self.model.objects.all().order_by('-Date_creation')
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects).order_by('-Date_creation')
        return queryset[:100]

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
                'page_obj': page_obj,
                'paginator': paginator
            },
            request=request
        )
        return JsonResponse({
            'success': True,
            'html': html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if self.form_class == RecensementsForm:
                recensement = form.save(commit=False)
                immeuble = recensement.Immeuble
                last_number = Recensements.objects.filter(Immeuble=immeuble).count()
                recensement.Numero = last_number + 1
                obj = form.save()
            else:
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
            return redirect(f'baux:{self.list_route}')
        except Locataires.DoesNotExist:
            messages.success(request, f"{self.model._meta.verbose_name} non trouvé !")
            return redirect(f'baux:{self.list_route}')

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

# generic partial view function :
class GenericPartialFormView(TemplateView):
    """
    Generic AJAX-based form handler for modal partials.
    Subclasses can override hooks for custom post-save logic.
    """
    form_class = None
    success_message = 'Enregistrement effectué avec succès'
    template_name = 'baux/partials/form_template.html'

    # === Utility hook methods you can override ===

    def get_success_html(self, instance, request):
        """Optional: return custom HTML (e.g., a table row) for the created instance."""
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    # === HTTP methods ===

    def get(self, request, *args, **kwargs):
        """Render the empty form HTML."""
        form = self.form_class()
        html = render_to_string(self.template_name, {'form': form}, request=request)
        return JsonResponse({'html': html})

    def post(self, request, *args, **kwargs):
        """Handle AJAX POST and return JSON (success + optional HTML)."""
        if not self.form_class:
            return JsonResponse({'success': False, 'message': 'Formulaire non défini'}, status=500)

        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            html_row = self.get_success_html(instance, request) or ""

            return JsonResponse({
                'success': True,
                'id': instance.id,
                'text': str(instance),
                'message': self.success_message,
                'html': html_row,
            })

        # invalid form → re-render errors
        html = render_to_string(self.template_name, {'form': form}, request=request)
        return JsonResponse({
            'success': False,
            'html': html,
            'message': 'Erreur lors de l\'enregistrement',
            'errors': form.errors,
        })
