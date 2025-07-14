"""Views handling user authentication requests."""

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Invalid credentials"})
        else:
            messages.error(request, "AJAX requests only.")
        return redirect('login_page_name')  # Adjust this with the login page's URL name
    return redirect('index')

@csrf_exempt
def user_logout(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        logout(request)
        return JsonResponse({"success": True})
    else:
        return redirect('index')
# authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegisterForm, ProfileEditForm
from .models import Profile

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                messages.error(request, "حساب شما هنوز فعال نشده است. لطفاً منتظر تأیید ادمین بمانید.")
                return redirect("login")
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "اطلاعات کاربری نادرست است.")
    return render(request, "authentication/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Form.save() creates the user, profile and group
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)

            # Consumers are activated without admin approval
            group_name = form.cleaned_data.get("group")
            if group_name == "consumer":
                user.is_active = True
            else:
                # Farmers and stakeholders require admin approval
                user.is_active = False

            user.save()

            # Save the Profile as well
            profile = Profile.objects.create(
                user=user,
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                group=group_name,
                country=form.cleaned_data.get("country"),
                farm_address=form.cleaned_data.get("farm_address") or ""
            )

            # Assign the Django group
            group_obj, _ = Group.objects.get_or_create(name=group_name.capitalize())
            user.groups.add(group_obj)

            # Display a suitable message to the user
            if group_name == "consumer":
                messages.success(request, "ثبت نام شما با موفقیت انجام شد. اکنون می‌توانید وارد شوید.")
            else:
                messages.success(request, "ثبت نام شما انجام شد. حساب‌تان پس از بررسی مدیر فعال می‌شود.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})

@login_required
def profile_edit_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت بروزرسانی شد.")
            return redirect("profile_edit")
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, "authentication/profile_edit.html", {"form": form})
