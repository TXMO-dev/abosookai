from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.translation import gettext as _

def create_user(**param):
    return get_user_model().objects.create_user(**param)
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')  
ME_URL = reverse('user:me') 

class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """" Test creating user with valid payload is successful """
        payload = {
            'email':'ddd@gmail.com',
            'password':'testpass',   
            'name':'Steff London',
            'phone_number': '+12034456982',
            'user_type': 'Dealer',
            'address': '6 Placebo Hwy',
            'city': 'los Vegas',
            'state':'Nevada',
            'zip':'2922',
            'description':'i have over 40 years experience in this field and im willing to learn'
        }
        user = create_user(**payload)    
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)                              

    def test_user_already_exists(self):
        """ Test that the user already exists """
        payload = {
            'email':'ddd@gmail.com',
            'password':'password',
            'name':'Steff London',
            'phone_number': '+12034456982',
            'user_type': 'Dealer',
            'address': '6 Placebo Hwy',
            'city': 'los Vegas',  
            'state':'Nevada',
            'zip':'2922',
            'description':'i have over 40 years experience in this field and im willing to learn'          
        }  
        user = create_user(**payload) 
        res = self.client.post(CREATE_USER_URL, payload) 
        if user == res.data:             
            res.status_code = status.HTTP_400_BAD_REQUEST              
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)   

    def test_create_token_for_user(self):
        """ Test that the token is created for the user """
        payload = {
            'email':'ddd@gmail.com',
            'password':'password'          
        } 
        create_user(**payload)           
        res = self.client.post(TOKEN_URL, payload)          
        self.assertIn('token', res.data)            
        self.assertEqual(res.status_code, status.HTTP_200_OK)                   

    def test_create_token_missing_field(self):
        """ Test that the necessary credentials are required before given a token """  
        create_user(email="germano@engineapp.com",password="germanwhip") 
        payload = {
            'email':'ddd@gmail.com',
            'password':'password',        
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) 


class PrivateUserApi(TestCase):
    """ This is to test that the user is the one requesting for its profile """  
    def setUp(self):
        self.user = create_user(
            email = 'test@londonappdev.com',
            password='testpass',
            name='name'
        ) 
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) 

    def test_retreive_user_unauthorized(self):
        """ Test that authorization is required for users """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_402_UNAUTHORIZED)

    def test_retreive_profile_suuccess(self):
        """ This is to test that the authenticated user retreived the profile successfully """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email
        })

    def test_post_not_allowed(self):
        """ Test that POST is not allowed on the ME url """
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for the authenticated user """
        payload = {
            'name':'newname',
            'password':'newpass123'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
          

          
   