from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("show_list",csrf_exempt(views.show_list), name="show_list"),
    path("show_post/<int:pk>",views.show_post, name="show_post"),
    path("show_following_posts/<str:user_id>",views.show_following_posts, name="show_following_posts"),
    path("show_user_posts/<str:user_posts>",views.show_user_posts,name="show_user_posts"),
    path("comments/<str:post_id>",views.comments, name="comments"),
    path("comment/<str:comment_pk>",views.comment, name="comment"),
    path("follow/<str:user_id>",views.follow, name="follow"),
    path("unfollow/<str:flwr>/<str:flwrd>",views.unfollow, name="unfollow"),
    path("like/<str:post_id>",views.like, name="like"),
    path("unlike/<str:post_id>/<str:user_id>",views.unlike, name="unlike"),
    path("ProfileView/<str:user_id>",views.ProfileView.as_view()),
    path("get_user_id/<str:username>", views.get_user_id),
    path("get_users_random/<str:pk>", views.get_users_random),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
