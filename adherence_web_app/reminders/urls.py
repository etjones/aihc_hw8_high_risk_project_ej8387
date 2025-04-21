from django.urls import path
from . import views

app_name = "reminders"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("circle_member/<int:pk>/edit/", views.edit_circle_member, name="edit_circle_member"),
    path("circle_member/<int:pk>/delete/", views.delete_circle_member, name="delete_circle_member"),
    path("circle_member/<int:circle_member_id>/prescription/add/", views.add_prescription, name="add_prescription"),
    path("prescription/<int:pk>/edit/", views.edit_prescription, name="edit_prescription"),
    path("prescription/<int:pk>/delete/", views.delete_prescription, name="delete_prescription"),
]
