from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import PostForm
from .models import Post
from django.urls import reverse_lazy
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_1.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    # ordering = 'title'
    template_name = 'post_1.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
# Create your views here.

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = "post_create.html"

    #def get_success_url(self):
        #return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_news',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_1.html')