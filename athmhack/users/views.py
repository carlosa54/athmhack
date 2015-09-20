from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login

from django.shortcuts import redirect
from .models import User
from ..items.models import Item
from ..invoices.models import InvoiceItem
from ..invoices.forms import InvoiceForm

import requests


def user_logout(request):
    logout(request)
    return redirect("/")


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class RegisterView(TemplateView):
    template_name = "accounts/register.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        card_number = request.POST.get('card_number', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        phone = request.POST.get('phone', None)

        name = first_name + last_name

        if password != password2:
            context["errors"] = "Passwords don't match!"
            return self.render_to_response(context)

        payload = {"username": username, "password": password,
                   "cardNumber": card_number, "isPublic": True,
                   "name": name, "phoneNumber": phone}
        headers = {"content-type": "application/json"}

        response = requests.post("http://54.175.166.76:8080/api/registerCustomer",
                                 headers=headers, json=payload)
        data = response.json()
        print data

        if data['responseStatus']['status'] == "SUCCESS":
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login')

            payload = {"username": username, "password": password}
            response = requests.post("http://54.175.166.76:8080/api/login",
                                     headers=headers, json=payload)
            data = response.json()
            if data['responseStatus']['status'] == "SUCCESS":
                print data
                print data['id']
                login(request, user)
                request.session['ath_id'] = data['id']
                return redirect('/')
            else:
                logout(request)
                return redirect('/login')
        else:
            context["errors"] = "Sorry! We could not register you to our Network."
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return redirect('/')
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = "accounts/login.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username or not password:
            context["errors"] = "Username or password is not correct."
            return self.render_to_response(context)

        headers = {'content-type': "application/json"}
        payload = {"username": username, "password": password}
        response = requests.post("http://54.175.166.76:8080/api/login",
                                 headers=headers, json=payload)
        data = response.json()
        if data['responseStatus']['status'] != "SUCCESS":
            context["errors"] = "Username or password is not correct."
            return self.render_to_response(context)

        user = authenticate(username=username, password=password)

        if user is None:
            context["errors"] = "Username or password is not correct."
            return self.render_to_response(context)
        login(request, user)
        request.session['ath_id'] = data['id']
        return redirect('/')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return redirect("/")
        return self.render_to_response(context)


class DashBoardView(TemplateView):
    template_name = "dashboard/index.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("/login")
        context = self.get_context_data(**kwargs)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            new_invoice = form.save(commit=False)
            new_invoice.biller = request.user

            items = {}
            for item in request.POST.items():
                prop = item[0].split("_")
                if len(prop) == 2:
                    prop_id = prop[1]
                    prop_exist = items.get(prop_id, None)
                    if prop_exist:
                        items[prop_id][prop[0]] = item[1]
                    else:
                        items[prop_id] = {}
                        items[prop_id][prop[0]] = item[1]

            print items

            new_invoice.save()

            for item in items.items():
                add_item = Item.objects.get(pk=item[1]['id'])
                invoice_item = InvoiceItem(item=add_item, invoice=new_invoice, quantity=item[1]['quantity'])
                invoice_item.save()

            new_invoice.send_invoice()
            context["success"] = "The Invoice was sent to the user"
        else:
            context["error"] = "The Invoice failed to be created."

        context = self.retrieve_client_and_items(request.user, context)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("/login")
        context = self.get_context_data(**kwargs)

        context = self.retrieve_client_and_items(request.user, context)
        return self.render_to_response(context)

    def retrieve_client_and_items(self, user, context):
        clients = User.objects.exclude(id=user.id)
        items = Item.objects.filter(user=user)
        context["clients"] = clients
        context["items"] = items
        return context
