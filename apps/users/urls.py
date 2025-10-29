from django.urls import path
from .views import *
from apps.baux.urls import get_crud_urls

urlpatterns = [
    *get_crud_urls(UserView, "utilisateur/utilisateurs", "utilisateur"),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/password/', UserPasswordView.as_view(), name='user_password_update'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('groups/', GroupAPIView.as_view(), name='api-groups'),
]
