from django.urls import reverse
from network.models import Comment, Follow, Like, Post, Profile, User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestViews(APITestCase):
    
    def setUp(self):
        # create user1 for test
       self.user1 = User.objects.create(username="bbhmed",password="1234cs50")
       # create user2 for test
       self.user2 = User.objects.create(username="sidi",password="2234cs50")
       # create post1 for test
       self.post1 = self.client.post(reverse('show_list'), data={
        "id": 1,
        "post": "cs50 web 1",
        "date": "2022-02-20T21:23:04.000270Z",
        "user": "bbhmed"
        })
        # create post2 for test
       self.post2 = self.client.post(reverse('show_list'), data={
        "id": 2,
        "post": "cs50 web 2",
        "date": "2022-02-20T21:23:04.000270Z",
        "user": "bbhmed"
        })
        # create comment on post1 for test
       self.comment = self.client.post(reverse('comments', args=[1]), data={
        "id": 1,
        "post": 1,
        "body":"comment on cs50 web 1",
        "date": "2022-02-20T21:23:04.000270Z",
        "user": "bbhmed"
        })
       self.response1 = self.client.post(reverse('follow', args=[1]), data={
        "id": 4,
        "following":1,
        "followed": 2,
        })



    ######## start post tests ##########

    def test_show_list(self):
        """ test POST a post """
        response = self.client.post(reverse('show_list'), data={
        "id": 3,
        "post": "cs50 web",
        "date": "2022-02-20T21:23:04.000270Z",
        "user": "bbhmed"
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_show_user_posts(self):
        """ test GET all post of specify user"""
        response = self.client.get(reverse('show_user_posts', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def show_following_posts(self):
        """ test GET all posts of all follows users"""
        response = self.client.get(reverse('show_following_posts', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post(self):
        """ test GET a post by id"""
        response = self.client.get(reverse('show_post', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["post"],"cs50 web 1")
        self.assertEqual(response.data["id"],1)
        
    def test_put_post(self):
        """ test PUT a post by id"""
        response = self.client.put(reverse('show_post', args=[1]), data={
            "id": 1,
            "post":"cs50 web 1 updated",
            "date": "2022-02-20T21:23:04.000270Z",
            "user": "bbhmed"
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_post(self):
        """ test DELETE a post by id"""
        response = self.client.delete(reverse('show_post', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

    ######## end post tests ##########

    ######## start comment tests ##########

    def test_comment_on_post1(self):
        """ test comment on post1 """
        response = self.client.post(reverse('comments', args=[1]), data={
        "id": 2,
        "post": 1,
        "body":"comment on cs50 web 1",
        "date": "2022-02-20T21:23:04.000270Z",
        "user": "sidi"
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_comment(self):
        """ test GET a comment by id"""
        response = self.client.get(reverse('comment', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["body"],"comment on cs50 web 1")
        self.assertEqual(response.data["id"],1)
        
    def test_put_comment(self):
        """ test PUT a comment by id"""
        response = self.client.put(reverse('comment', args=[1]), data={
            "id": 1,
            "post": 1,
            "body":"updated comment on cs50 web 1",
            "date": "2022-02-20T21:23:04.000270Z",
            "user": "bbhmed"
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_comment(self):
        """ test DELETE a comment by id"""
        response = self.client.delete(reverse('comment', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        

    ######## end comment tests ##########

    ######## start follow unfollow tests ##########

    def test_follow(self):
        """ test user1 follow user2 """
        response1 = self.client.post(reverse('follow', args=[1]), data={
        "id": 1,
        "following":1,
        "followed": 2
        })
        response2 = self.client.get(reverse('follow', args=[1]))
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data["follows"], 2)
    
    
    def test_unfollow(self):
        """test user1 unfollow user2 """
        response = self.client.delete(reverse('unfollow', args=[1,2]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
        
       

    ######## end follow unfolllow tests ##########

    ######## start like unlike tests ##########

    def test_like(self):
        """ test user1 like post1 """
        response1 = self.client.post(reverse('like', args=[1]), data={
        "id": 1,
        "user":1,
        "post": 1
        })
        response2 = self.client.get(reverse('like', args=[1]))
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data["Likes"], 1)
    
        
    def test_unlike(self):
        """ test user1 unlike pos1 """
        response1 = self.client.post(reverse('like', args=[1]), data={
        "id": 1,
        "user":1,
        "post": 1
        })
        response = self.client.delete(reverse('unlike', args=[1,1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
        
    ######## end like unlike tests ##########
