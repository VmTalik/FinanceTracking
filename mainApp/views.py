from django.views.generic import CreateView, View, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm
from django.shortcuts import render
from .services.mixins import UserIsNotAuthenticated


class UserRegisterView(UserIsNotAuthenticated, SuccessMessageMixin, CreateView):
    """Представление регистрации на сайте с формой регистрации"""
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'mainApp/register.html'
    success_message = 'Вы успешно зарегистрировались. Теперь можете осуществить вход в личный кабинет!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """Авторизация на сайте"""
    form_class = UserLoginForm
    template_name = 'mainApp/login.html'
    next_page = 'profile'
    success_message = 'Добро пожаловать в личный кабинет, здесь Вы можете отслеживать свои расходы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """Выход с личного кабинета"""
    next_page = 'home'


class ProfileView(LoginRequiredMixin, View):
    """Личный кабинет пользователя"""

    def get(self, request):
        return render(request, 'mainApp/profile.html', context={'data': 123})


class MainView(TemplateView):
    """Главная страница сайта"""
    template_name = 'mainApp/index.html'
