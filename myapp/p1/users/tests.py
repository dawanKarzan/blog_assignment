import json
from django.test import TestCase
from rest_framework import status
from .serializers import AuthorSerializer, RoleSerializer, AdminSerializer

class AppTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.role_data = {
            "name": "Admin",
            "description": "Administrator role",
            "can_read": True,
            "can_create": True,
            "can_update": True,
            "can_delete": True
        }
        cls.role_data2 = {
            "name": "Admin 2",
            "description": "Administrator role",
            "can_read": True,
            "can_create": True,
            "can_update": False,
            "can_delete": True
        }
        roleSer = RoleSerializer(data=cls.role_data)
        roleSer.is_valid(raise_exception=True)
        role = roleSer.save()
        cls.role_id = role.id
        cls.admin_data2 = {
            "email": "admin26@email.com",
            "password": "12345678",
            "phone_number": "0987654321",
            "role": cls.role_id,
            "username": "admin2",
            "first_name": "admin",
            "last_name": "last admin",
            "is_staff": True
        }
        cls.admin_data_invalid = {
            "email": "admin25@email.com",
            "password": "12345678",
            "phone_number": "0987654321",
            "role": cls.role_id,
            "username": "admin",
            "first_name": "admin",
            "last_name": "last admin",
            "is_staff": True
        }
        cls.admin_data = {
            "email": "admin25@email.com",
            "password": "12345678",
            "phone_number": "0987654321",
            "role": cls.role_id,
            "username": "admin",
            "first_name": "admin",
            "last_name": "last admin",
            "is_staff": True
        }
        adminSer = AdminSerializer(data=cls.admin_data)
        adminSer.is_valid(raise_exception=True)
        admin =adminSer.save()
        cls.admin_id = admin.id
        cls.author_data2 = {
            "email": "dawankarzan19@gmail.com",
            "password": "12345678",
            "username": "author",
            "phone_number": "0987654321",
            "first_name": "author",
            "last_name": "last author",
            "is_staff": False
        }
        cls.author_data = {
            "email": "dawankarzan18@gmail.com",
            "password": "12345678",
            "username": "author2",
            "phone_number": "0987654321",
            "first_name": "author",
            "last_name": "last author",
            "is_staff": False
        }
        cls.author_data3 = {
            "email": "dawankarzan538@gmail.com",
            "password": "12345678",
            "username": "author32",
            "phone_number": "0987654321",
            "first_name": "author33",
            "last_name": "last author",
            "is_staff": False
        }
        cls.author_data_invalid = {
            "email": "dawankarzan18@gmail.com",
            "username": "author2",
            "phone_number": "0987654321",
            "first_name": "author",
            "last_name": "last author",
            "is_staff": False
        }
        cls.author_data_updated = {
            "first_name": "author updated",
            "last_name": "last author updated"
        }
        authorSer = AuthorSerializer(data=cls.author_data)
        authorSer.is_valid(raise_exception=True)
        author = authorSer.save()
        cls.author_id = author.id
        cls.verify_code = author.verification_code
        cls.author_to_verify = {
            "email": "dawankarzan18@gmail.com",
            "verification_code": cls.verify_code
        }
        cls.data_password_updated = {
            "password": "87654321",
            "old_password": "12345678"
        }
        cls.admin_authenticated_data = {
            "email": "admin25@email.com",
            "password": "12345678"
        }
        cls.author_authenticated_data = {
            "email": "dawankarzan18@gmail.com",
            "password": "12345678"
        }

    def setUp(self) -> None:
        super().setUp()
        admin = json.dumps(self.__class__.admin_authenticated_data)
        adminAuth = self.client.post('/users/api/token/', data=admin, content_type='application/json')
        self.assertEqual(adminAuth.status_code, status.HTTP_200_OK)
        self.admin_token = adminAuth.data['access']
        self.admin_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.admin_token}'
        }

        response = self.client.post('/users/verify-email/', self.author_to_verify, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author_auth = self.client.post('/users/api/token/', data=self.__class__.author_authenticated_data)
        self.assertEqual(author_auth.status_code, status.HTTP_200_OK)
        self.author_token = author_auth.data['access']
        self.author_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.author_token}'
        }


    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_author_not_found(self):
        res = self.client.post('/register/', self.author_data2, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(1,1)

    def test_author_create_valid(self):
        res = self.client.post('/users/register/', self.author_data2, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_author_verify(self):
        authorSer3 = AuthorSerializer(data=self.author_data3)
        authorSer3.is_valid(raise_exception=True)
        author3 = authorSer3.save()
        self.author_to_verify3 = {
            "email": "dawankarzan538@gmail.com",
            "verification_code": author3.verification_code
        }
        res = self.client.post('/users/verify-email/',data= self.author_to_verify3, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_create_invalid(self):
        res = self.client.post('/users/register/', self.author_data_invalid, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_update_valid(self):
        # print('self . author_data_updated', self.author_data_updated)
        # print('self . author_headers', self.author_headers)
        author_data_updated = json.dumps(self.author_data_updated)
        # print('author_data_updated', author_data_updated)
        res = self.client.put(f'/users/user/{self.author_id}/', author_data_updated, headers=self.author_headers, content_type='application/json')
        # print("test_author_update_valid res", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_not_authorized(self):
        res = self.client.get('/users/user/', self.author_data2, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_get_specific(self):
        res = self.client.get(f'/users/user/{self.author_id}/', headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_author_get_all(self):
        res = self.client.get('/users/user/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
  
    def test_author_update_password(self):
        data_password_updated = json.dumps(self.data_password_updated)
        res = self.client.put(f'/users/update-author-password/{self.author_id}/', data = data_password_updated, headers=self.author_headers, content_type='application/json')
        # print("test_author_update_valid res", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_author_delete(self):
        res = self.client.get(f'/users/user/{self.author_id}/', self.author_data2, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_not_found(self):
        res = self.client.post('/custom-admin/', self.admin_data2, content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_create_valid(self):
        admin_data2 = self.admin_data2 
        res = self.client.post('/users/custom-admin/', data=admin_data2, headers=self.admin_headers, content_type='application/json')
        # print("res", res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_create_invalid(self):
        res = self.client.post('/users/custom-admin/', self.admin_data_invalid, content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_update_valid(self):
        # print('self . author_data_updated', self.author_data_updated)
        # print('self . author_headers', self.author_headers)
        author_data_updated = json.dumps(self.author_data_updated)
        # print('author_data_updated', author_data_updated)
        res = self.client.put(f'/users/custom-admin/{self.admin_id}/', author_data_updated, headers=self.admin_headers, content_type='application/json')
        # print("test_author_update_valid res", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_not_authorized(self):
        res = self.client.get('/users/custom-admin/', self.admin_data2, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_get_specific(self):
        res = self.client.get(f'/users/custom-admin/{self.admin_id}/', headers=self.admin_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_admin_get_all(self):
        res = self.client.get('/users/custom-admin/', content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_update_password(self):
        data_password_updated = json.dumps(self.data_password_updated)
        res = self.client.put(f'/users/update-admin-password/{self.admin_id}/', data=data_password_updated, headers=self.admin_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_admin_delete(self):
        res = self.client.get(f'/users/custom-admin/{self.admin_id}/', content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



    def test_role_not_found(self):
        res = self.client.post('/role/', self.role_data2, content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_role_create_valid(self):
        role_data2 = self.role_data2 
        res = self.client.post('/users/role/', data=role_data2, headers=self.admin_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_role_update_valid(self):
        role_data2 = json.dumps(self.role_data2)
        res = self.client.put(f'/users/role/{self.role_id}/', role_data2, headers=self.admin_headers, content_type='application/json')

    def test_role_not_authorized(self):
        res = self.client.get('/users/role/', self.role_data2, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_role_get_specific(self):
        res = self.client.get(f'/users/role/{self.role_id}/', headers=self.admin_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_role_get_all(self):
        res = self.client.get('/users/role/', content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_role_delete(self):
        res = self.client.get(f'/users/role/{self.role_id}/', content_type='application/json', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_author_all_not_found(self):
        res = self.client.post('/author-all/', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_author_all_update_valid(self):
        author = json.dumps(self.author_data_updated)
        res = self.client.put(f'/users/admin/author-all/{self.author_id}/', data=author, headers=self.admin_headers, content_type='application/json')
        # print("test_author_update_valid res", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_author_all_not_authorized(self):
        res = self.client.get('/users/admin/author-all/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_author_all_get_specific(self):
        res = self.client.get(f'/users/admin/author-all/{self.author_id}/', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_admin_author_all_get_all(self):
        res = self.client.get('/users/admin/author-all/', headers=self.admin_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)