from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout, views
from django.views.generic import RedirectView, edit

from .forms import UserRegistrationForm
from .models import CustomUser, Manager, Employee


class LoginView(views.LoginView):
    template_name = 'user/login.html'
    login_url = '/login'
    next_page = None

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        user = self.request.user
        groups = user.groups.all()
        if groups.filter(name='customer').exists():
            return reverse_lazy('sales:sales_list')
        return reverse_lazy('inventory:product_list')


class LogoutView(RedirectView):
    pattern_name = 'users:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignUpView(edit.CreateView):
    template_name = 'user/register.html'
    success_url = '/login'
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = self.request.path
        if 'empleado' in url:
            context['employee_account'] = True
        elif 'cliente' in url:
            context['customer_account'] = True
        return context

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['use_required_attribute'] = False
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        account_type = self.request.POST.get('account_type')
        if account_type == 'employee':
            user.save()
            group = Group.objects.get(name='employee')
            user.groups.add(group)
        elif account_type == 'customer':
            user.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
        messages.success(
            self.request,
            f'Empleado "{user}" creado con éxito'
        )
        return super().form_valid(form)
