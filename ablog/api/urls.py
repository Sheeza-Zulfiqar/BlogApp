from django.urls import path,include
from .views import ListPost,DetailPost,ListComment,DetailComment,UserList,UserDetail,\
    DraftPost,DetailDraftPost,MyPosts,ListAllComment,MyApi
from rest_framework import routers
from api.views import CommentViewSet



router = routers.SimpleRouter()
router.register(r'comment', CommentViewSet)

#
urlpatterns=[
    path('',include(router.urls)),
    path('posts/',ListPost.as_view(),name='posts'),
    path('p/',MyApi.as_view(),name='p'),
    path('posts/draft/',DraftPost.as_view(),name='draft_posts'),
    path('myposts/',MyPosts.as_view(),name='my_posts'),
    path('posts/<int:pk>/',DetailPost.as_view(),name='single_post'),
    path('posts/draft/<int:pk>/',DetailDraftPost.as_view(),name='single_draft_post'),
    path('comments/',ListComment.as_view(),name='comments'),
    path('comments/<int:pk>/',DetailComment.as_view(),name='single_comment'),
    path('allcomments/<int:pk>/',ListAllComment.as_view(),name='all_comments'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]