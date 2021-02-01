from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView

from apps.accounts.forms import SignUpForm
from apps.accounts.mixins import RedirectAuthenticatedMixin, CurrentUserObjectMixin


class SignUpView(RedirectAuthenticatedMixin, CreateView):
    form_class = SignUpForm
    template_name = 'pages/auth/signup.html'
    success_url = reverse_lazy('homepage')
    redirect_url = success_url

    def form_valid(self, form):
        self.object = form.save()

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        if email and password:
            user = authenticate(self.request, email=email, password=password)
            if user:
                login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class CustomLoginView(LoginView):
    template_name = 'pages/auth/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    template_name = 'pages/auth/logout.html'
