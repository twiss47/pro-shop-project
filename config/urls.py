from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views  

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN & LOGOUT (project-level)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', users_views.register_view, name='register'), 


    # App URLs
    path('', include('app.urls', namespace='app')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
