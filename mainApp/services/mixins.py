from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class UserIsNotAuthenticated(UserPassesTestMixin):
    """Предотвращение посещения страницы регистрации авторизованных пользователей."""
    def test_func(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return True
     
    def handle_no_permission(self):
        return redirect('home')