from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileView, MainView, AddExpenseView, \
    UpdateExpenseView, ExpenseListView, ExpenseDeleteView

urlpatterns = [
    path('profile/update_expense/<int:expense_id>/', UpdateExpenseView.as_view(), name='update_expense'),
    path('profile/delete_expense/<int:expense_id>/', ExpenseDeleteView.as_view(), name='delete_expense'),
    path('profile/add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('profile/expenses/', ExpenseListView.as_view(), name='expenses'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', MainView.as_view(), name='home')
]
