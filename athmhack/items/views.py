from django.shortcuts import render
from .forms import ItemForm
from django.views.generic import TemplateView 
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect

class ItemView(TemplateView):
	title = 'Item'
	template_name = 'items/item.html'

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		form = ItemForm(request.POST)

		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		form = ItemForm()
		context = self.get_context_data(**kwargs)
		# if not request.user.is_authenticated():
		#	return redirect("/login")
		return self.render_to_response(context)