from network.models import Comment, Follow, Like, Post, Profile, User

from .test_setUp import TestSetUp


class TestModels(TestSetUp):
    
    def test_create_user_profile(self):
        """assert that func create a profile automatic when a user created"""
        self.usr_data = { 
            'username':'harvard',
            'email':'harvard@harvard.com',
            'password':'harvard2022',
            'confirmation':'harvard2022',
        }
        self.client.post(self.register_url, self.usr_data, format="json")
        self.usr = User.objects.get(username="harvard")
        profile = Profile.objects.get(user=self.usr)
        self.assertTrue(profile)

    def test_profile_names_label(self):
        """assert that profile label working well"""
        res = Profile.objects.get(pk=1)
        f_label1 = res._meta.get_field('description').verbose_name
        f_label2 = res._meta.get_field('user').verbose_name
        f_label3 = res._meta.get_field('img').verbose_name
        self.assertEqual(f_label1,'description')
        self.assertEqual(f_label2,'user')
        self.assertEqual(f_label3,'img')

    def test_profile_str(self):
        """assert that profile str method working well"""
        res = Profile.objects.get(pk=1)
        self.assertEqual(str(res),"etar")

    def test_post_str(self):
        """assert that post str method working well"""
        res = Post.objects.create(user=self.us,post="hello cs50")
        self.assertEqual(str(res),"etar post")

    def test_post_names_label(self):
        """assert that post label names working well"""
        
        res = Post.objects.get(pk=1)
        f_label1 = res._meta.get_field('post').verbose_name
        f_label2 = res._meta.get_field('user').verbose_name
        f_label3 = res._meta.get_field('date').verbose_name
        self.assertEqual(f_label1,'post')
        self.assertEqual(f_label2,'user')
        self.assertEqual(f_label3,'date')

    def test_comment_str(self):
        """assert that comment str method working well"""
        res = Post.objects.create(user=self.us,post="hello cs50")
        comment = Comment.objects.create(user=self.us,post=res)
        self.assertEqual(str(comment),"etar commnted on etar post .")

    def test_comment_names_label(self):
        """assert that comment label names working well"""
        res = Comment.objects.get(pk=1)
        f_label1 = res._meta.get_field('post').verbose_name
        f_label2 = res._meta.get_field('user').verbose_name
        f_label3 = res._meta.get_field('date').verbose_name
        f_label4 = res._meta.get_field('body').verbose_name
        self.assertEqual(f_label1,'post')
        self.assertEqual(f_label2,'user')
        self.assertEqual(f_label3,'date')
        self.assertEqual(f_label4,'body')

    def test_like_str(self):
        """assert that like str method working well"""
        res = Post.objects.create(user=self.us,post="hello cs50")
        like = Like.objects.create(user=self.us2,post=res)
        self.assertEqual(str(like),"bbhmed liked etar post .")

    def test_like_names_label(self):
        """assert that like label names working well"""
        res = Like.objects.get(pk=1)
        f_label1 = res._meta.get_field('post').verbose_name
        f_label2 = res._meta.get_field('user').verbose_name
      
        self.assertEqual(f_label1,'post')
        self.assertEqual(f_label2,'user')
       

    def test_follow_str(self):
        """assert that follow str method working well"""
        res = Follow.objects.create(following=self.us,followed=self.us2)
        self.assertEqual(str(res),"etar following bbhmed .")
    
    def test_follow_names_label(self):
        """assert that follow label names working well"""
        res = Follow.objects.get(pk=1)
        f_label1 = res._meta.get_field('following').verbose_name
        f_label2 = res._meta.get_field('followed').verbose_name
        f_label3 = res._meta.get_field('val').verbose_name
        self.assertEqual(f_label1,'following')
        self.assertEqual(f_label2,'followed')
        self.assertEqual(f_label3,'val')

    