from django.urls import path
from .views import *

urlpatterns = [
	path('', posts_list, name='posts_list_url'),
	path('post/create/', PostCreate.as_view(), name='post_create_url'),
	path('post/<str:slug>/', PostDetail.as_view(), name='post_details_url'),
	path('post/<str:slug>/delete', PostDelete.as_view(), name='post_delete_url'),
	path('post/<str:slug>/update', PostUpdate.as_view(), name='post_update_url'),
	# скобки означают что при попадании каких либо символов после post/ захватывать символы в slug
	path('tags/', tags_list, name='tags_list_url'),
	path('tag/create/', TagCreate.as_view(), name = 'tag_create_url'),
	path('tag/<str:slug>/', TagDetail.as_view(), name='tag_details_url'),
	path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
	path('tag/<str:slug>/update/', TagUpdate.as_view(), name = 'tag_update_url'),
]

