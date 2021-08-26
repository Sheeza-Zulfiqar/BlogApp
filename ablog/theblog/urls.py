from .import views
from django.urls import path
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.urls import login
from django.contrib.auth import views
from .views import PostListView,PostDetailView,UserProfileView,signup,login\
    ,SearchView,    AboutView,post_publish,CreatePostView,\
    add_comment_to_post,DraftListView,comment_approve,comment_remove,PostDeleteView,PostUpdateView,user_logout,user_login

    # ListPost,RetrieveUpdateDestroyPost,RetrieveUpdateDestroyComment,  ListCreateComment,\


urlpatterns = [
    path('',PostListView.as_view(),name='home'),
    # path('api/',ListPost.as_view(),name='api_post_list'),
    # path('api/<int:pk>',RetrieveUpdateDestroyPost.as_view(),name='api_post_detail'),
    # path('api/<post_pk>/comment/',ListCreateComment.as_view(),name='api_add_comment'),
    # path('api/<post_pk>/comment/<pk>',RetrieveUpdateDestroyComment.as_view(),name='api_add_comment_detail'),
    path('register/', signup, name='signup'),
    path('login/', user_login, name='signin'),
    # path('login/',views.LoginView.as_view() , name='login'),
    path('results/', SearchView.as_view(), name='search'),
    path('logout/',user_logout,name='user_logout'),
    path('myposts/',UserProfileView.as_view(),name='my_posts'),
    path('about/',AboutView.as_view(),name='about'),
    path('post/<int:pk>',PostDetailView.as_view(),name='post_detail'),
    path('post/<int:pk>/publish/',post_publish,name='post_publish'),
    path('post/new/',CreatePostView.as_view(),name='post_new'),
    path('post/<int:pk>/comment/',add_comment_to_post,name='add_comment_to_post'),
    path('drafts/',DraftListView.as_view(),name='post_draft_list'),
    path('comment/<int:pk>/approve/',comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('post/<int:pk>/edit/',PostUpdateView.as_view(),name='update_post'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='delete_post'),
]