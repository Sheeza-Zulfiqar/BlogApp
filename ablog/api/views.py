from django.shortcuts import render
from theblog.models import Post,Comment
from rest_framework.views import APIView
# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import PostSerializer,CommentSerializer,RegistrationSerializer,UserSerializer,PostChildSerializer,AllCommentSerializer,DraftPostSerializer,MyPostSerializer
from django.db.models import Count,Case,When
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404,redirect
from rest_framework import serializers
import uuid
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .permissions import IsOwnerOrReadOnly,IsOwner,IsSuperUser
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
# Create your views here.

from django.contrib.auth.models import User



class MyApi(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        postdata = {"data": []}
        postdata_c = {"data": []}
        for p in Post.objects.filter(published_date__isnull=False):
            c = Comment.objects.filter(approved_comment=True, post__id=p.id).values_list('id', flat=True)
            cc = Comment.objects.filter(approved_comment=True, post__id=p.id).values_list('text',flat=True)
            comments = list(cc)
            cl = list(c)

            count = len(cl)
            post = {}
            post["id"] = p.id
            post["title"] = p.title
            post["text"] = p.text
            post["TotalComments"] = count
            postdata["data"].append(post)
            post_c = {}
            post_c["id"] = p.id
            post_c["title"] = p.title
            post_c["text"] = p.text
            post_c["TotalComments"] = count
            post_c["Comments"] = comments
            postdata_c["data"].append(post_c)

        if self.request.user.is_authenticated:
            return Response(postdata_c)

        return Response(postdata)

class CommentViewSet(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.filter(approved_comment=True)
    serializer_class = AllCommentSerializer
    pagination_class = [PageNumberPagination]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class RegistrationApiView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self,request):
        serialzer=self.get_serializer(data=request.data)
        # serialzer.is_valid(raise_exception=True)
        # serialzer.save()
        if(serialzer.is_valid()):
            serialzer.save()
            return Response({
                "RequestId":str(uuid.uuid4()),
                "Message": "User created successfully",
                "User": serialzer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"Errors": serializers.errors},status=status.HTTP_400_BAD_REQUEST)

        # return Response({"User":serialzer.data,})


class ListPost(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        postdata = {"data": []}
        postdata_c = {"data": []}

        for p in Post.objects.filter(published_date__isnull=False):
            c = Comment.objects.filter(approved_comment=True, post__id=p.id).values_list('id', flat=True)
            cc = Comment.objects.filter(approved_comment=True, post__id=p.id).values_list('text', flat=True)
            comments = list(cc)
            cl = list(c)

            count = len(cl)
            post = {}
            post["id"] = p.id
            post["title"] = p.title
            post["text"] = p.text
            post["TotalComments"] = count
            postdata["data"].append(post)
            post_c = {}
            post_c["id"] = p.id
            post_c["title"] = p.title
            post_c["text"] = p.text
            post_c["TotalComments"] = count
            post_c["Comments"] = comments
            postdata_c["data"].append(post_c)

        if self.request.user.is_authenticated:
            return Response(postdata_c)

        return Response(postdata)



    serializer_class = PostSerializer

    # def get_serializer_class(self):
    #
    #     if self.request.user.is_authenticated and   self.request.method == 'POST':
    #         return PostSerializer
        # elif not self.request.user.is_authenticated:
        #     return PostChildSerializer
# annotate
#     post_obj_list=Post.objects.filter(published_date__isnull=False).values_list('id', flat=True)
#     common_ids= Post.objects.filter(id__in=Comment.objects.filter(approved_comment=True).values_list('post_id', flat=True)).values_list('id', flat=True)
#     p_c=Post.objects.all().filter(id__in=common_ids)
#
#
#
#     # cc=Commenclt.objects.filter(id__in=)
#     coments_count = Comment.objects.all().filter(post_id__in=post_obj_list)

    # queryset = Post.objects.filter(published_date__isnull=False)
    # queryset = Post.objects.raw('SELECT "theblog_post"."id", "theblog_post"."author_id", "theblog_post"."title", "theblog_post"."text", "theblog_post"."create_date", "theblog_post"."published_date", COUNT(CASE WHEN "theblog_comment"."approved_comment" THEN 1 ELSE NULL END) AS "TotalComments" FROM "theblog_post" LEFT OUTER JOIN "theblog_comment" ON ("theblog_post"."id" = "theblog_comment"."post_id") WHERE "theblog_post"."published_date" IS NOT NULL GROUP BY "theblog_post"."id", "theblog_post"."author_id", "theblog_post"."title", "theblog_post"."text", "theblog_post"."create_date", "theblog_post"."published_date"')
    # queryset = Post.objects.filter(published_date__isnull=False).annotate(TotalComments=Count(Case(When(comments__approved_comment=True, then=1))))
    # def get_serializer_context(self):
    #     context = super(ListPost, self).get_serializer_context()
    #     context.update({'comments': Comment.objects.all()})
    #     return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    # post = get_object_or_404(Post, pk=kwargs['question_id'])

    def get_serializer_class(self):
        if not self.request.user.is_authenticated and self.request.method == 'GET':
            return PostChildSerializer
        else:
            return PostSerializer
    queryset = Post.objects.all().filter(published_date__isnull=False).annotate(TotalComments=Count(Case(When(comments__approved_comment=True, then=1))))

    # def get(self, request, *args, **kwargs):
    #     p = get_object_or_404(Post, pk=kwargs['pk'])
    #     postdata = {"data": []}
    #
    #     post_c = {}
    #     post_c["id"] = p.id
    #     post_c["title"] = p.title
    #     post_c["text"] = p.text
    #     post_c["create_date"] = p.create_date
    #     post_c["published_date"] = p.published_date
    #     # post_c["TotalComments"] = count
    #     # post_c["Comments"] = comments
    #     postdata["data"].append(post_c)
    #     #
    #     # if self.request.user.is_authenticated:
    #     #     return Response(postdata_c)

        # return Response(postdata)



    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class DraftPost(generics.ListAPIView):
    serializer_class = DraftPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner,IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).filter(published_date__isnull=True).order_by('create_date')

class DetailDraftPost(generics.RetrieveUpdateAPIView):
    serializer_class = DraftPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner,IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).filter(published_date__isnull=True).order_by('create_date')

class ListComment(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(approved_comment=True)
    serializer_class = AllCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DetailComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(approved_comment=True)
    serializer_class = AllCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class MyPosts(generics.ListAPIView):
    serializer_class = MyPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner,IsAuthenticated]
    queryset = Post.objects.all()


    pagination_class = PageNumberPagination
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class ListAllComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

