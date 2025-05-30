"""
URL configuration for adherence_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from reminders import views as reminders_views

urlpatterns = [
    # Home page
    path("", reminders_views.home, name="home"),
    # Admin site
    path("admin/", admin.site.urls),
    # Reminders app (custom registration)
    path("reminders/", include("reminders.urls", namespace="reminders")),
    # Django built-in auth views (login, logout, password reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
    # Profile page
    path("accounts/profile/", reminders_views.profile, name="profile"),
    path("__reload__/", include("django_browser_reload.urls")),
]
