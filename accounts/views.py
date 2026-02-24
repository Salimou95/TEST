"""Views for the accounts app: registration, login, logout, profile."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect("store:product_list")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Bienvenue {user.username} ! Votre compte a été créé."
            )
            return redirect("store:product_list")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect("store:product_list")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            next_url = request.GET.get("next", "store:product_list")
            return redirect(next_url)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "accounts/login.html")


def user_logout(request):
    """Log out the current user."""
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("store:product_list")


@login_required
def profile(request):
    """Display and update the user's profile."""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        "accounts/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
