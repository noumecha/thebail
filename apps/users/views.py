from django.views.generic import TemplateView, View
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .forms import *
from .serializers import GroupSerializer, UserSerializer
from web_project import TemplateLayout
from config.views import *
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages
from web_project import TemplateLayout
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import models
from django.core.paginator import Paginator
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


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

# login view
class LoginView(View):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, {})
        return context

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # ✅ Création des tokens JWT
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            response = redirect("index")
            # ✅ Cookies sécurisés
            response.set_cookie(
                "access_token", access,
                httponly=True, secure=not settings.DEBUG,
                samesite="Lax", max_age=60*60
            )
            response.set_cookie(
                "refresh_token", str(refresh),
                httponly=True, secure=not settings.DEBUG,
                samesite="Lax", max_age=60*60*24*7
            )
            login(request, user)
            return response

        return render(request, self.template_name, {"error": "Identifiants invalides"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect('login')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

# api view
class LoginAPIView(TokenObtainPairView):
    """
    Authentifie l’utilisateur et crée les cookies JWT (access + refresh).
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access = data.get('access')
            refresh = data.get('refresh')

            # ✅ Crée la réponse finale avec cookies sécurisés
            res = Response({'message': 'Connexion réussie'}, status=status.HTTP_200_OK)
            res.set_cookie(
                'access_token',
                access,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=60 * 15  # 15 min
            )
            res.set_cookie(
                'refresh_token',
                refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=60 * 60 * 24 * 7  # 7 jours
            )
            return res
        return response

class LogoutAPIView(APIView):
    """
    Supprime les cookies JWT.
    """
    def post(self, request):
        res = Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res

# user CRUD view
class UserView(BaseCRUDView):
    model = Utilisateur
    form_class = UtilisateurForm
    list_route = 'utilisateur_list'
    list_template = "user_list.html"
    filters = [
        ('role', RoleUtilisateur),
    ]
    context_object_name = 'users'
    search_fields = ['username', 'first_name']
    headers = ["Nom", "Prenom", "Role", "Email"]
    fields = ['username', 'first_name', 'role', 'email']
    delete_url = "utilisateur_delete"

class GroupAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = RoleUtilisateur.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

# users views
class UserProfileView(TemplateView):
    template_name = "user_profile.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class UserPasswordView(TemplateView):
    template_name = "user_password_update.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
