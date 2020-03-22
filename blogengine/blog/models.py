from django.db import models
from django.shortcuts import reverse #генерирует ссылку

from django.utils.text import slugify #  для генерации слагов
from time import time

def gen_slug(s):
	"""Генерация слага и уникализация его через time"""
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))


class Post(models.Model):
	"""Описание класса постов"""
	title = models.CharField(max_length=150, db_index=True)# db_index <-- индексация
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	body = models.TextField(blank=True, db_index=True) # означает что поле может быть пустым
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts') # пост может не иметь тегов, relatedname обозначает свойство кот имеет Tag (эквивалентно post_set())
	date_pub = models.DateTimeField(auto_now_add=True) # Время при добавлении

	class Meta:
		ordering =  ['-date_pub']# Порядок сортировки

	def get_absolute_url(self):
		"""Возвращает ссылку на конкретный обьект (экземпляр класса пост)"""
		return reverse('post_details_url', kwargs={'slug' : self.slug})
		# reverse - это тоже самое что и url в href=''

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug' : self.slug})

	def get_create_url(self):
		return reverse('post_create_url', kwargs={'slug' : self.slug})


	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug' : self.slug})


	def save(self, *args, **kwargs):
		"""Переопределения save для того что бы сохранение производилось только при создании поста"""
		# для этого воспользуемся свойством того, что только при сохранении экземпляр получает id
		if not self.id:
			self.slug = gen_slug(self.title)
		# Super - models.Model
		super().save(*args,**kwargs)

	def __str__(self):
		return self.title


class Tag(models.Model):
	"""класс тег"""
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True)

	class Meta:
		ordering =  ['title']

	def get_absolute_url(self):
		return reverse('tag_details_url', kwargs={ 'slug': self.slug })

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug' : self.slug})

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug' : self.slug})


	def get_create_url(self):
		return reverse('tag_create_url', kwargs={'slug' : self.slug})


	def __str__(self):
		return self.title