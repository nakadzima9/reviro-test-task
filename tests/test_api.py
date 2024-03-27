from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from management.models import Company, Product


class CompanyApiTest(APITestCase):
    def setUp(self):
        self.test_data = {
            'title': 'Valid data',
            'description': 'Valid test data',
            'location': 'J 240 s.right',
            'schedule': '8:30-17:30',
        }

        self.test_update_data = {
            'title': 'Updated data',
            'description': 'Updated description',
            'location': 'J 240 s.right',
            'schedule': '8:30-17:30',
        }

        self.test_partial_update_data = {
            'title': 'Valid title'
        }

        self.test_invalid_data = {
            'title': '',
            'description': '',
            'location': 'J 240 s.right',
            'schedule': '8:30-17:30',
        }

        self.company = Company.objects.create(
            title="Test case",
            description="Test case description",
            location="L 120 right and left",
            schedule="8:00-17:00"
        )

    def test_create_company(self):
        url = reverse('company-list')
        response = self.client.post(url, self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Company.objects.get(pk=2).title, self.test_data['title'])

    def test_company_list(self):
        url = reverse('company-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_company_detail(self):
        url = reverse('company', kwargs={"pk": self.company.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.company.pk)
        self.assertEqual(response.data['title'], self.company.title)

    def test_company_update(self):
        url = reverse('company', kwargs={"pk": self.company.pk})
        response = self.client.put(url, self.test_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(response.data['id'], self.company.pk)
        self.assertEqual(response.data['title'], self.company.title)
        self.assertEqual(self.test_update_data['title'], self.company.title)
        self.assertEqual(self.test_update_data['description'], self.company.description)

    def test_company_partial_update(self):
        url = reverse('company', kwargs={'pk': self.company.pk})
        response = self.client.patch(url, self.test_partial_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(response.data['id'], self.company.pk)
        self.assertEqual(response.data['title'], self.company.title)
        self.assertEqual(self.test_partial_update_data['title'], self.company.title)

    def test_company_delete(self):
        url = reverse('company', kwargs={'pk': self.company.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)

    def test_company_create_invalid(self):
        url = reverse('company-list')
        response = self.client.post(url, self.test_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 1)


class ProductApiTest(APITestCase):
    def setUp(self):
        self.test_data = {
            'title': 'Valid data',
            'description': 'Valid test data',
            'price': 100,
            'quantity': 50,
            'attachment': 1,
        }

        self.test_update_data = {
            'title': 'Updated data',
            'description': 'Updated test data',
            'price': 100,
            'quantity': 50,
            'attachment': 1,
        }

        self.test_partial_update_data = {
            'title': 'Valid title',
        }

        self.test_invalid_data = {
            'title': '',
            'description': '',
            'price': 100,
            'quantity': 50,
            'attachment': 1,
        }

        self.product = Product.objects.create(
            title="Test case",
            description="Test case description",
            price=100,
            quantity=50,
            attachment=Company.objects.create(
                title='Valid data',
                description='Valid test data',
                location='J 240 s.right',
                schedule='8:30-17:30'
            ),
        )

    def test_create_product(self):
        url = reverse('product-list')
        response = self.client.post(url, self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(pk=2).title, self.test_data['title'])

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['attachment']['title'], Company.objects.get(pk=1).title)

    def test_product_detail(self):
        url = reverse('product', kwargs={"pk": self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.pk)
        self.assertEqual(response.data['title'], self.product.title)

    def test_product_update(self):
        url = reverse('product', kwargs={"pk": self.product.pk})
        response = self.client.put(url, self.test_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(response.data['id'], self.product.pk)
        self.assertEqual(response.data['title'], self.product.title)
        self.assertEqual(response.data['price'], self.product.price)
        self.assertEqual(self.test_update_data['title'], self.product.title)
        self.assertEqual(self.test_update_data['description'], self.product.description)
        self.assertEqual(self.test_update_data['price'], self.product.price)

    def test_product_partial_update(self):
        url = reverse('product', kwargs={"pk": self.product.pk})
        response = self.client.patch(url, self.test_partial_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(response.data['id'], self.product.pk)
        self.assertEqual(response.data['title'], self.product.title)
        self.assertEqual(self.test_partial_update_data['title'], self.product.title)

    def test_product_delete(self):
        url = reverse('product', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_create_invalid(self):
        url = reverse('company-list')
        response = self.client.post(url, self.test_invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 1)
