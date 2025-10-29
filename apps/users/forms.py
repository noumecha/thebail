from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from dal import autocomplete, forward
from django.template.loader import render_to_string


class LoginForm(AuthenticationForm):
    # Add any custom fields or modifications here
    pass

# users form
class UtilisateurForm(forms.ModelForm):
    # Password fields
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirmation mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez le mot de passe'}),
        required=False,
    )

    class Meta:
        model = Utilisateur

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
        )
        labels = {
            'username': "Login utilisateur",
            'first_name': "Prénom utilisateur",
            'last_name': "Nom utilisateur",
            'email': "Email utilisateur",
            'role': "Rôle",
            'is_active': "Compte actif/inactif",
        }

        widgets = {
            'Date_delivrance_cni': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(UtilisateurForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['is_active'].help_text = None

        # Make password required only for new users
        if not self.instance.pk:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            self.fields['password1'].help_text = "Le mot de passe doit contenir au moins 8 caractères"

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            Fieldset(
                'Informations personnelles',
                Row(
                    Column(FloatingField("username"), css_class='form-group col-md-6 mb-3'),
                    Column(FloatingField("email"), css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
                Row(
                    Column(FloatingField("first_name"), css_class='form-group col-md-6 mb-3'),
                    Column(FloatingField("last_name"), css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Mot de passe',
                Row(
                    Column(FloatingField("password1"), css_class='form-group col-md-6 mb-3'),
                    Column(FloatingField("password2"), css_class='form-group col-md-6 mb-3'),
                    css_class='form-row'
                ),
            ),
            Fieldset(
                'Rôles et Statut',
                Row(
                    Column(FloatingField("role"), css_class='form-group col-md-6 mb-3'),
                    Column(Field('is_active'), css_class='form-group col-md-6 mb-0',),
                    css_class='form-row'
                ),
            ),
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Les deux mots de passe ne correspondent pas.")

            # Validate password strength
            if len(password1) < 8:
                raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email exists for other users
            users = Utilisateur.objects.filter(email=email)
            if self.instance.pk:
                users = users.exclude(pk=self.instance.pk)
            if users.exists():
                raise ValidationError("Un utilisateur avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # Handle password
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            # Save many-to-many relationships (groups)
            self.save_m2m()

        return user
