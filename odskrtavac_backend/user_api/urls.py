from django.urls import path
from .views import RegisterView, LogoutView, get_user_rights
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user_api"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('get-user-rights/', get_user_rights, name='get_user_rights'),  # Ensure this is a function-based view
]
