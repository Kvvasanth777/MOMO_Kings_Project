from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UserForm, ProfileForm
from .models import CustomerProfile, User


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('landing')
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.get_or_create(user=user)
            from menu.models import Wishlist
            from orders.models import Cart
            Wishlist.objects.get_or_create(user=user)
            Cart.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to Momo Kings, {user.username}!")
            return redirect('landing')
        return render(request, 'accounts/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('landing')
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('landing')
        messages.error(request, "Invalid username or password.")
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('landing')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile, created = CustomerProfile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile)
        from orders.models import Order
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        from menu.models import Wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.items.all()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'orders': orders,
            'wishlist_items': wishlist_items
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request):
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile, created = CustomerProfile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        from orders.models import Order
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        from menu.models import Wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.items.all()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'orders': orders,
            'wishlist_items': wishlist_items
        }
        return render(request, 'accounts/profile.html', context)


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'accounts/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        request.session['reset_email'] = email
        request.session['mock_otp'] = '123456'
        messages.success(request, "OTP sent to your email (Use '123456' for verification).")
        return redirect('verify_otp')


class VerifyOTPView(View):
    def get(self, request):
        return render(request, 'accounts/verify_otp.html')

    def post(self, request):
        otp = request.POST.get('otp')
        if otp == request.session.get('mock_otp'):
            messages.success(request, "OTP Verified. Please reset your password.")
            return redirect('profile')
        messages.error(request, "Invalid OTP. Please try again.")
        return render(request, 'accounts/verify_otp.html')
