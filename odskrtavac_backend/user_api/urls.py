from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, LogoutView

app_name = "user_api"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
