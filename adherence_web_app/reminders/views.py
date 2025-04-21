from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccountHolderRegistrationForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user

def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AccountHolderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect(reverse("login"))
    else:
        form = AccountHolderRegistrationForm()
    return render(request, "registration/register.html", {"form": form})

def home(request: HttpRequest) -> HttpResponse:
    user = get_user(request)
    if user.is_authenticated:
        return redirect("/reminders/dashboard/")
    return render(request, "home.html")

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard.html")

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "profile.html")
