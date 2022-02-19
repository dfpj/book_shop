from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy

from .forms import UserLoginForm,UserCreationForm
from .models import User



class UserLoginView(View):
    form_class =UserLoginForm
    template_name = 'accounts/login.html'

    def get(self,request):
        return render(request,self.template_name, {'form_accounts': self.form_class})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            user = authenticate(request,email=cd['email'],password=cd['password1'])
            if user is not None:
                login(request,user)
                messages.success(request,"logged successfuly",'info')
                return redirect('book:home')
            messages.error(request, "email or password is wrong", 'warning')
        return render(request, self.template_name, {'form_accounts':form})

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.error(request, "logout successfuly", 'info')
        return redirect('book:home')



class UserRegisterView(View):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form_accounts': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(email=cd['email'], password=cd['password1'])
            messages.success(request, "register successfuly", 'info')
            return redirect('book:home')
        return render(request, self.template_name, {'form_accounts': form})


class UserPasswordResetView(PasswordResetView):
    template_name='accounts/password_reset_form.html'
    email_template_name ='accounts/password_reset_email.html'
    success_url=reverse_lazy('accounts:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name ='accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'