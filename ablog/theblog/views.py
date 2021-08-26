from django.shortcuts import render
from .models import Post,Comment
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,CommentForm,SignUpForm
from django.contrib.auth import login,logout
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect,HttpResponse,Http404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import mixins
from django.core.exceptions import PermissionDenied
# Create your views here./19
# List view basically allow us a list basicaly allow us a query set into the database...it will do a query set for us look up all the records in the database and bring them back that we can list out
# detail view same as list view make query set to a database but it just bring out one record the details of one record
# ListView--All our blog posts DetailView--detail of One blog post
#######################################
# class ListPost(APIView):
#     # format controls the format that comes back out
#     def get(self,request,format=None):
#         post=Post.objects.all()
#         serializer=serializers.PostSerializer(post,many=True)
#         return Response(serializer.data)
#     def post(self,request,format=None):
#         serializer=serializers.PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
# class ListPost(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
# class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class=serializers.PostSerializer
#
# class ListCreateComment(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentSerializer
#
#     def get_queryset(self):
#         return self.queryset.filter(post_id=self.kwargs.get('post_pk'))
#     def perform_create(self, serializer):
# #         runs when view created
#         post=get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
#         serializer.save(post=post)
#
#
# class RetrieveUpdateDestroyComment(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class=serializers.CommentSerializer
#
#     def get_object(self):
#         return get_object_or_404(
#             self.queryset(),
#             post_id=self.kwargs.get('post_pk'),
#             pk=self.kwargs.get('pk')
#         )
#
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
#
#     @action(detail=True, methods=['get'])
#     def comments(self,request,pk=None):
#         self.pagination_class.page_size=1
#         comments=Comment.objects.filter(approved_comment=True,post_id=pk)
#         page=self.paginate_queryset(comments)
#         if page is not None:
#             serializer=serializers.CommentSerializer(page,many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer=serializers.CommentSerializer(
#            comments,many=True
#         )
#         return Response(serializer.data)
#
#
# class CommentViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentSerializer
#
#
#
#
#
#







#######################################################################################################
def signup(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                # login(request, user)
                messages.success(request, "Registration successful." )
                return redirect("signin")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = SignUpForm()
        return render(request=request, template_name="register.html", context={"form":form})
    elif request.user.is_authenticated:
        return redirect('home')


def user_login(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # elif not request.user.is_authenticated:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                request.session['is_logged'] = True
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form":form})

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("home"))

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def home(request):
    return render(request,'home.html',{})

class AboutView(TemplateView):
    template_name = 'about.html'



class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-published_date']
    # queryset = my_get_queryset()

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('signin')
        else:
            return super(PostDetailView, self).dispatch(request,*args,**kwargs)

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/signin/'
    redirect_field_name = 'post_detail.html'
    template_name = 'post_form.html'
    form_class = PostForm
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('signin')
        else:
            return super().dispatch(request,*args, **kwargs)

    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/signin/'
    # redirect_field_name = 'home.html'
    template_name = 'update_post.html'
    fields = ['title','text']
    model = Post
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.request.user.is_authenticated:
            return redirect('signin')
        elif obj.author != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        else:
            return super().dispatch(request,*args, **kwargs)
    success_url = reverse_lazy('home')

class SearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            user = self.request.user
            postresult = Post.objects.filter(title__contains=query).filter(author=user)
            result = postresult
        else:
            result = None
        return result

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/signin/'
    redirect_field_name = 'home.html'


    template_name = 'post_draft_list.html'
    context_object_name = 'draft_posts'
    model = Post
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('signin')
        else:
            return super().dispatch(request,*args, **kwargs)
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'delete_post.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.request.user.is_authenticated:
            return redirect('signin')
        elif self.request.user.is_authenticated and not self.request.user.is_superuser and obj.author != self.request.user:
            raise Http404("You are not allowed to delete this Post")
        elif self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif not self.request.user.is_superuser or obj.author == self.request.user:
            return super().dispatch(request,*args, **kwargs)
    success_url = reverse_lazy('home')



class UserProfileView(LoginRequiredMixin, ListView):

     #queryset = Post.objects.all()
     template_name = "my_posts.html"
     context_object_name = 'all_posts'
     # ordering = 'id'user = self.request.user
     def dispatch(self, request, *args, **kwargs):
         if not self.request.user.is_authenticated:
             return redirect('signin')
         else:
             return super().dispatch(request, *args, **kwargs)

     def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).order_by('-id')

# def user_posts(request,pk):
#     post = get_object_or_404(Post, pk=pk)
#     all_posts = post.objects.filter(posti=request.user)
#     return render(request,'my_posts.html',all_posts)
#

# @login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # user = get_object_or_404(User, pk=pk)
    if not request.user.is_authenticated:
        return redirect('signin')

    # user_comments = post.comments.filter(author=request.user.username)
    # if request.user.is_authenticated:
    #     username=request.user.username
    # if user_comments:
    #     # If there are any, raise an errorauthor
    #     raise PermissionDenied('You have already commented on this post.')

    #######################################
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated and request.user==post.author:
        post.publish()
        return redirect('post_detail', pk=pk)
    else:
        return redirect('signin')

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated:
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)
    else:
        return redirect('signin')

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('home')
    else:
        return redirect('signin')