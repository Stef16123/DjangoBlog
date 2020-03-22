from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .models import *
from .forms import *

class ObjectDetailMixin:
	model = None
	template = None

	def get(self, request, slug):
		obj = get_object_or_404(self.model, slug__iexact=slug)
		context = {self.model.__name__.lower(): obj, 'admin_object' : obj, 'detail' : True} # берем имя класса и хуярим в нижний регистр
		return render(request, self.template, context)


class ObjectCreateMixin:
	model = None
	template = None

	def get(self, request):
		form = self.model()
		context = {'form' : form }
		return render(request, self.template , context)

	def post(self, request):
		bound_form = self.model(request.POST)
		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)

		else:
			context = {'form' : bound_form}
			return render(request, self.template, context)

class ObjectUpdateMixin:
	model = None
	model_form = None
	template = None

	def get(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.model_form(instance=obj) # Вставляем в форму данные из модели тег
		context = {'form' : bound_form,  self.model.__name__.lower() : obj}
		return render(request, self.template, context)

	def post(self,request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.model_form(request.POST, instance=obj)
		if bound_form.is_valid():
			up_obj = bound_form.save()
			return redirect(up_obj)
		else:
			context = {'form' : bound_form, self.model.__name__.lower() : obj}
			return render(request, self.template, context)

class ObjectDeleteMixin:
	model = None
	template = None
	url_name = None

	def get(self,request,slug):
		obj = self.model.objects.get(slug__iexact=slug)
		context = {self.model.__name__.lower() : obj}
		return render(request, self.template, context)

	def post(self, request, slug):
		obj = self.model.objects.get(slug__iexact=slug)
		obj.delete()
		return redirect(reverse(self.url_name))
	