from django.shortcuts import render
from .forms import ItemForm
from .models import Item
from django.views.generic import TemplateView 
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect

class AddItemView(TemplateView):
	template_name = 'items/item.html'
	
	def post(self, request, *args, **kwargs):
		
		if not request.user.is_authenticated():
			return redirect("/login")
		context = self.get_context_data(**kwargs)
		form = ItemForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
			context['success'] = "Item succsessfuly added"
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		
		if not request.user.is_authenticated():
			return redirect("/login")
		context = self.get_context_data(**kwargs)
		# if not request.user.is_authenticated():
		#	return redirect("/login")
		return self.render_to_response(context)

class EditItemView(TemplateView):
	template_name = 'items/edit.html'
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return redirect("/login")
		context = self.get_context_data(**kwargs)
		
		form = ItemForm(request.POST)
		if form.is_valid():
			item = Item.objects.get(pk= 4)
			item_form = ItemForm(request.POST, instance = item)
			item_form.save()
			context['success'] = "Item succsessfuly added"
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		items = Item.objects.filter(user = request.user)
		context = self.get_context_data(**kwargs)
		context['items'] = items
		if not request.user.is_authenticated():
			return redirect("/login")
		return self.render_to_response(context)