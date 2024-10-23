from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book-api/', include('books.urls')),
    path('user-api/', include('user_api.urls')),
]

