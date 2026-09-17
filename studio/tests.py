from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Order


class OrderAdminListTests(TestCase):
    def test_order_string_representation_includes_name_and_service(self):
        user = User.objects.create_user(username='buyer', password='secret')
        order = Order.objects.create(
            user=user,
            name='Ali Valiev',
            phone='+998901234567',
            service='Veb-sayt',
            website_info='Sayt kerak',
            budget='2000',
        )

        self.assertEqual(str(order), 'Ali Valiev (Veb-sayt)')

    def test_admin_order_list_shows_customer_details_and_action_buttons(self):
        admin = User.objects.create_user(username='admin', password='secret', is_staff=True)
        user = User.objects.create_user(username='buyer', password='secret')
        order = Order.objects.create(
            user=user,
            name='Ali Valiev',
            phone='+998901234567',
            telegram='@alivaliev',
            service='Veb-sayt',
            website_info='Sayt kerak',
            budget='2000',
        )

        self.client.force_login(admin)
        list_response = self.client.get(reverse('admin_list', args=['zakazlar']))
        detail_response = self.client.get(reverse('admin_order_reply', args=[order.pk]))

        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'Ali Valiev')
        self.assertContains(list_response, '+998901234567')
        self.assertContains(list_response, 'Ko‘rish')
        self.assertContains(list_response, 'Tahrirlash')
        self.assertContains(list_response, 'O‘chirish')

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Javob yozish')
        self.assertContains(detail_response, 'Javobni yuborish')

    def test_logout_form_has_confirm_and_redirects_home(self):
        user = User.objects.create_user(username='buyer', password='secret')
        self.client.force_login(user)

        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'data-logout-form="true"')

        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('home'))
