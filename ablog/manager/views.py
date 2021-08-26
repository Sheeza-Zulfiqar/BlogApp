from django.shortcuts import render
# from theblog.models import Post,Comment
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
# Create your views here.
# class PostListView(ListView):
#     model = Post
#
#     template_name = 'all_users_posts.html'
#     ordering = ['-published_date']
    # queryset = my_get_queryset()