from django.views.generic import CreateView, View, TemplateView, UpdateView, DetailView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm
from django.shortcuts import get_object_or_404, render
from .services.mixins import UserIsNotAuthenticated
from .models import Expense, Category, User
from .forms import ExpenseForm
from .utilities import classifier


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
        expenses = Expense.objects.all()
        return render(request, 'mainApp/profile.html', context={'expenses': expenses})


class MainView(TemplateView):
    """Главная страница сайта"""
    template_name = 'mainApp/index.html'


class AddExpenseView(CreateView):
    """Добавление расхода"""
    model = Expense
    form_class = ExpenseForm
    template_name = 'mainApp/add_expense.html'

    def form_valid(self, form):
        description = form.cleaned_data.get('description')
        nlp = classifier.run_classifier()  # определяем категорию расхода с помощью NLP
        doc = nlp(description)
        res = doc.cats
        max_predicted = max(res, key=res.get)  # обнаруженное название категории
        category, created = Category.objects.get_or_create(name=max_predicted)  #
        form.instance.category_id = category
        form.instance.user_id = get_object_or_404(User, pk=self.request.user.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')


class UpdateExpenseView(UpdateView):
    """Обновление расхода"""
    model = Expense
    form_class = ExpenseForm
    template_name = 'mainApp/update_expense.html'
    pk_url_kwarg = 'expense_id'

    def get_success_url(self):
        return reverse_lazy('profile')


class ExpenseListView(ListView):
    """Список расходов"""
    model = Expense
    template_name = 'mainApp/expenses.html'


class ExpenseDeleteView(DeleteView):
    """Удаление расхода"""
    model = Expense
    pk_url_kwarg = 'expense_id'
    success_url = reverse_lazy('expenses')
    template_name = 'mainApp/delete_expense.html'
