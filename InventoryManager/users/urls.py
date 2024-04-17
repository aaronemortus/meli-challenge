from django.urls import path, reverse_lazy

from .views import LoginView, LogoutView, SignUpView


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True, next_page=reverse_lazy('inventory:product_list')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alta_empleado/', SignUpView.as_view(), name='register_employee'),
    path('alta_cliente/', SignUpView.as_view(), name='register_customer'),
]