from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import TagForm, PostForm
from .models import Post, Tag
from .utils import *



def posts_list(request):
	"""Обработка списка постов"""
	search_query = request.GET.get('search', '')

	if search_query:
		posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
	else:
		posts = Post.objects.all()

	# posts = Post.objects.all()
	paginator = Paginator(posts, 10)


	page_number = request.GET.get('page', 1) # Взять из запроса словарь GET и из словаря взять параметр page, 1 - это страница поумолчанию
	page = paginator.get_page(page_number)
	
	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''
	# отоброзить список обьектов для 1 страницы
	context = {
		"posts": page,
		"is_paginated" : is_paginated,
		"next_url " : next_url,
		"prev_url" : prev_url
	
	} 


	return render(request, 'blog/index.html', context)


# Благодаря миксином сокраща. запись для 2 обработчиков
class PostDetail(ObjectDetailMixin, View):	
	model = Post
	template = 'blog/post_details.html'
	
class TagDetail(ObjectDetailMixin, View):
	model = Tag
	template = 'blog/tag_details.html'
	

def tags_list(request):
	"""Обработка спиоков тегов"""
	tags = Tag.objects.all()
	context = {'tags' : tags}
	return render(request, 'blog/tags_list.html', context)


class PostCreate(LoginRequiredMixin,ObjectCreateMixin, View):
	model = PostForm
	template = 'blog/post_create.html'
	raise_exception = True

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
	model = TagForm
	template = 'blog/tag_create.html'
	raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model = Tag
	model_form = TagForm
	template = 'blog/tag_update.html'
	raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model = Post
	model_form = PostForm
	template = 'blog/post_update.html'
	raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin,View):
	model = Tag
	template = 'blog/tag_delet.html'
	url_name = 'tags_list_url'
	raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin,View):
	model = Post
	template = 'blog/post_delet.html'
	url_name = 'posts_list_url'
	raise_exception = True