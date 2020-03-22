from django import forms
from .models import Tag, Post
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):
	"""Форма для тега"""
	# title = forms.CharField(max_length=50)
	# slug = forms.CharField(max_length=50)
	class Meta:
		'''Берем из БД тэг и используем для формирования тег форм'''
		model = Tag
		fields = ['title', 'slug']

	def clean_slug(self):
		"""Приводим очищенное поле слаг в нижний регистр"""
		new_slug = self.cleaned_data['slug'].lower()
		if new_slug == 'create':
			raise ValidationError('slug not be create')
		
		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError('Slug is not unique')

		return new_slug

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['title', 'body', 'slug', 'tags']

		def clean_slug(self):
			new_slug = self.cleaned_data['slug'].lower()
			if new_slug == 'create':
				raise ValidationError('kek')
			return new_slug