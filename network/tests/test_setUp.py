from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase
from network.models import Comment, Follow, Like, Post, Profile, User

class TestSetUp(TestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = { 
            'username':'etar',
            'email':'bbhmed@gm.com',
            'password':'email@1',
            'confirmation':'email@1',
        }
        self.user2_data = { 
            'username':'bbhmed',
            'email':'bbhmed@gmd.com',
            'password':'email@12',
            'confirmation':'email@12',
        }
        self.client.post(self.register_url, self.user_data, format="json")
        self.us = User.objects.get(pk=1)
        self.client.post(self.register_url, self.user2_data, format="json")
        self.us2 = User.objects.get(pk=2)
        
        """for models test"""
        post = Post.objects.create(user=self.us, post="bla")
        like = Like.objects.create(user=self.us2,post=post)
        follow = Follow.objects.create(following=self.us2,followed=self.us)
        comment = Comment.objects.create(user=self.us2,post=post,body="bla")
        return super().setUp()


    def tearDown(self):
        return super().tearDown()