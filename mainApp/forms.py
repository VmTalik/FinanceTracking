from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Expense
from django.forms.widgets import NumberInput


class UserRegisterForm(UserCreationForm):
    """Переопределенная форма регистрации пользователей"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы регистрации"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Укажите логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Укажите пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите ввод пароля'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

    def clean_email(self):
        """Проверка email на уникальность"""
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')

        return email

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')


class UserLoginForm(AuthenticationForm):
    """Форма авторизации на сайте"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы регистрации"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['username'].label = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),
                           label='Дата расхода',
                           required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}),
                                  label='Описание',
                                  required=True)

    class Meta:
        model = Expense
        fields = ('value', 'description', 'date')
