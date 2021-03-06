from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from customer.models import CustomerContact

User = get_user_model()


class LoginTest(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_user(username='yertas', password='Durulit123',
                                                   is_superuser=True, is_staff=True,
                                                   email='yusufertas@hotmail.com')
        self.regular_user = User.objects.create_user(username='yusuf', password='tatatat123',
                                                     email='yusufertas@hotmail.com')
        self.client = APIClient()

    def test_login(self):
        login_result_1 = self.client.login(username='yertas', password='Durulit123', email='yusufertas@hotmail.com')
        login_result_2 = self.client.login(username='yusuf', password='tatatat123', email='yusufertas@hotmail.com')
        assert login_result_1 is True
        assert login_result_2 is True


class CustomerSuperUserTest(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_user(username='yertas', password='Durulit123',
                                                   is_superuser=True, email='yusufertas@hotmail.com')
        self.regular_user = User.objects.create_user(username='yusuf', password='tatatat123',
                                                     email='yusufertas@hotmail.com')
        self.super_token = Token.objects.create(user=self.super_user)
        self.regular_token = Token.objects.create(user=self.regular_user)
        self.client = APIClient()
        assert User.objects.all().count() == 2

    def test_customer_database(self):
        # Create a customer with superuser account
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        self.client.post('/api/customer_contact/', {
            'user_id': 1,
            'first_name': 'Metin',
            'last_name': 'Ertas',
            'phone': '123',
            'email': 'metin@mt.com'
        }, format='json')
        response_super = self.client.post('/api/customer/', {'first_name': 'Metin',
                                                             'last_name': 'Ertas',
                                                             'phone': '123',
                                                             'company': 'Acme',
                                                             'email': 'metin@mt.com',
                                                             'reference': 'Mustafa Ertas',
                                                             'user_id': 1
                                                             }, format='json')
        assert response_super.status_code in [200, 201]

        # Create a customer with regular account
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        self.client.post('/api/customer_contact/', {
            'user_id': 2,
            'first_name': 'Mustafa',
            'last_name': 'Ertaasdasds',
            'phone': '123445',
            'email': 'yusufertas@hotmail.com'
        }, format='json')
        response_regular = self.client.post('/api/customer/', {'first_name': 'Mustafa',
                                                               'last_name': 'Ertaasdasds',
                                                               'phone': '123445',
                                                               'company': 'Sony',
                                                               'email': 'yusufertas@hotmail.com',
                                                               'reference': 'John Ertas',
                                                               "user_id": 2
                                                               }, format='json')
        assert response_regular.status_code in [200, 201]

        # Get customer for superuser should be the entire list
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        response_super = self.client.get('/api/customer/').json()
        print(response_super)
        assert len(response_super) == 2
        assert response_super[0]['phone'] == '123'
        assert response_super[1]['phone'] == '123445'

        # Get customer for regular user should be only the 2nd customer which is created by this user.
        # Hence a regular user should only be able to see the users they created.
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        response_regular = self.client.get('/api/customer/').json()
        # print(response_regular)
        assert len(response_regular) == 1
        assert response_super[1]['phone'] == '123445'

        # Retrieving customers for superuser:
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        response_super_1 = self.client.get('/api/customer/1/')
        print(response_super_1.json())
        response_super_2 = self.client.get('/api/customer/2/')
        assert response_super_1.status_code, response_super_2.status_code == (200, 200)
        assert response_super_1.json()['phone'] == '123'
        assert response_super_2.json()['last_name'] == 'Ertaasdasds'

        # Retrieving Customers for regular user:
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        response_super_1 = self.client.get('/api/customer/1/')
        print(response_super_1.json())
        response_super_2 = self.client.get('/api/customer/2/')
        assert response_super_1.status_code, response_super_2.status_code == (403, 200)
        assert response_super_2.json()['last_name'] == 'Ertaasdasds'

        # Update both customers for superuser:
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        response_super_1 = self.client.patch('/api/customer/1/', {'first_name': 'Metims',
                                                                  'last_name': 'Dellas',
                                                                  'user_id': 1
                                                                  }, format='json')
        print(response_super_1)
        response_super_2 = self.client.patch('/api/customer/2/', {'first_name': 'Mstsd',
                                                                  'last_name': 'Ertas',
                                                                  'user_id': 2
                                                                  }, format='json')
        print(response_super_1, response_super_2)
        assert (response_super_1.status_code, response_super_2.status_code) == (200, 200) or \
               (response_super_1.status_code, response_super_2.status_code) == (201, 201)
        assert response_super_1.json()['last_name'] == 'Dellas'
        assert response_super_2.json()['last_name'] == 'Ertas'

        # Update for customers with regular user:
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        response_super_1 = self.client.patch('/api/customer/1/', {'first_name': 'Metin',
                                                                  'last_name': 'Welas',
                                                                  'user_id': 1
                                                                  }, format='json')
        response_super_2 = self.client.patch('/api/customer/2/', {'first_name': 'Mstsdsd',
                                                                  'last_name': 'Erhahdsh',
                                                                  'user_id': 2
                                                                  }, format='json')
        assert (response_super_1.status_code, response_super_2.status_code) == (403, 200) or \
               (response_super_1.status_code, response_super_2.status_code) == (403, 201)
        assert response_super_2.json()['last_name'] == 'Erhahdsh'


class LogTest(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_user(username='yertas', password='Durulit123',
                                                   is_superuser=True, email='yusufertas@hotmail.com')
        self.regular_user = User.objects.create_user(username='yusuf', password='tatatat123',
                                                     email='yusufertas@hotmail.com')
        self.super_token = Token.objects.create(user=self.super_user)
        self.regular_token = Token.objects.create(user=self.regular_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)

        self.client.post('/api/customer_contact/', {
            'user_id': 1,
            'first_name': 'Metin',
            'last_name': 'Ertas',
            'phone': '123',
            'email': 'metin@mt.com'
        }, format='json')
        self.client.post('/api/customer/', {'first_name': 'Metin',
                                            'last_name': 'Ertas',
                                            'phone': '123',
                                            'company': 'Acme',
                                            'email': 'metin@mt.com',
                                            'reference': 'Mustafa Ertas',
                                            'user_id': 1
                                            }, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        self.client.post('/api/customer_contact/', {
            'user_id': 2,
            'first_name': 'Mustafa',
            'last_name': 'Ertaasdasds',
            'phone': '123445',
            'email': 'yusufertas@hotmail.com'
        }, format='json')
        self.client.post('/api/customer/', {'first_name': 'Mustafa',
                                            'last_name': 'Ertaasdasds',
                                            'phone': '123445',
                                            'company': 'Sony',
                                            'email': 'yusufertas@hotmail.com',
                                            'reference': 'John Ertas',
                                            "user_id": 2
                                            }, format='json')

    def test_logs(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        response_super = self.client.post('/api/log/', {'user_id': 1,
                                                        'customer_id': 1,
                                                        'log': 'Will call later'},
                                          format='json')
        assert response_super.status_code in (200, 201)

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        response_regular = self.client.post('/api/log/', {'user_id': 2,
                                                          'customer_id': 2,
                                                          'log': 'Will call back soon'},
                                            format='json')
        assert response_regular.status_code in (200, 201)

        # Both users should be able to see the logs list for both logs created:
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        response_super = self.client.get('/api/log/')

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.super_user)
        response_regular = self.client.get('/api/log/')
        assert response_super.status_code, response_regular.status_code == (200, 200)
        assert len(response_super.json()), len(response_regular.json()) == (2, 2)
        assert response_super.json()[0]['log'], response_regular.json()[1]['log'] == (
            'Will call later',
            'Will call back soon'
        )


class RegistrationSignalTest(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_user(username='yertas', password='Durulit123',
                                                   is_superuser=True, email='yusufertas@hotmail.com')
        self.regular_user = User.objects.create_user(username='yusuf', password='tatatat123',
                                                     email='yusufertas@hotmail.com')
        self.super_token = Token.objects.create(user=self.super_user)
        self.regular_token = Token.objects.create(user=self.regular_user)

        self.client = APIClient()

    def test_customer_registration_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        contact_response = self.client.post('/api/customer_contact/', {
            'user_id': 2,
            'first_name': 'Mustafa',
            'last_name': 'Ertaas',
            'phone': '123445',
            'email': 'yusufertas@hotmail.com'
        }, format='json')
        print(contact_response)
        assert contact_response.status_code in (200, 201)
        assert contact_response.json()['first_name'] == 'Mustafa'

        self.client.post('/api/customer/', {'first_name': 'Mustafa',
                                            'last_name': 'Ertaas',
                                            'phone': '123445',
                                            'company': 'Sony',
                                            'email': 'yusufertas@hotmail.com',
                                            'reference': 'John Ertas',
                                            "user_id": 2
                                            }, format='json')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Url which contains the registration link')
        self.assertEqual(mail.outbox[0].body, 'Please register through this link')

    def test_customer_contact_update(self):
        # Testing whether updating the customer updates the relevant customer contact as well.
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.super_token))
        self.client.force_authenticate(self.super_user)
        self.client.post('/api/customer_contact/', {
            'user_id': 1,
            'first_name': 'Mustafa',
            'last_name': 'Ertaas',
            'phone': '123445',
            'email': 'yusufertas@hotmail.com'
        }, format='json')
        self.client.post('/api/customer/', {'first_name': 'Mustafa',
                                            'last_name': 'Ertaas',
                                            'phone': '123445',
                                            'company': 'Sony',
                                            'email': 'yusufertas@hotmail.com',
                                            'reference': 'John Ertas',
                                            "user_id": 1
                                            }, format='json')

        response_super_1 = self.client.patch('/api/customer/1/', {'first_name': 'Metims',
                                                                  'last_name': 'Dellas',
                                                                  'user_id': 1
                                                                  }, format='json')
        assert response_super_1.status_code in (200, 201)
        print(CustomerContact.objects.get(user__id=1).first_name)
        assert CustomerContact.objects.get(user__id=1).first_name == 'Metims'
        assert CustomerContact.objects.get(user__id=1).last_name == 'Dellas'

        # Tests whether regular user has permisson to do perform this action:

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.regular_token))
        self.client.force_authenticate(self.regular_user)
        self.client.post('/api/customer_contact/', {
            'user_id': 1,
            'first_name': 'Mustafa',
            'last_name': 'Ertaas',
            'phone': '123445',
            'email': 'yusufertas@hotmail.com'
        }, format='json')
        self.client.post('/api/customer/', {'first_name': 'Mustafa',
                                            'last_name': 'Ertaas',
                                            'phone': '123445',
                                            'company': 'Sony',
                                            'email': 'yusufertas@hotmail.com',
                                            'reference': 'John Ertas',
                                            "user_id": 1
                                            }, format='json')

        response_regular_1 = self.client.patch('/api/customer/1/', {'first_name': 'Metims',
                                                                    'last_name': 'Dellas',
                                                                    'user_id': 1
                                                                    })
        assert response_regular_1.status_code == 403
