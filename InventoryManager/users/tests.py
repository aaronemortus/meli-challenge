from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from .models import CustomUser, Manager, Employee, Customer
from .forms import UserRegistrationForm


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='password')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'test_user')
        self.assertTrue(self.user.check_password('password'))

    def test_manager_creation(self):
        manager = Manager.objects.create(profile=self.user)
        self.assertEqual(manager.profile.username, 'test_user')

    def test_employee_creation(self):
        employee = Employee.objects.create(profile=self.user)
        self.assertEqual(employee.profile.username, 'test_user')

    def test_customer_creation(self):
        customer = Customer.objects.create(profile=self.user)
        self.assertEqual(customer.profile.username, 'test_user')


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='password')

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)

    def test_signup_view(self):
        response = self.client.get(reverse('users:register_employee'))
        self.assertEqual(response.status_code, 200)


class UserFormsTestCase(TestCase):
    def test_user_registration_form(self):
        form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'password',
            'password2': 'password'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
