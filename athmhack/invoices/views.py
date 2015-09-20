from django.views.generic import TemplateView
from django.shortcuts import redirect

from .forms import InvoiceForm
from ..items.models import Item
from ..users.models import User
from .models import Invoice, InvoiceItem

import requests


class AddInvoiceView(TemplateView):
    template_name = "invoices/add_invoice.html"

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


class RetrieveInvoiceView(TemplateView):
    template_name = "invoices/invoice.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            invoice = Invoice.objects.get(pk=kwargs['pk'])
            context["invoice"] = invoice
            context["items"] = InvoiceItem.objects.filter(invoice=invoice)
            if not request.user.is_authenticated():
                return redirect("/login")
            if not invoice.paid:
                ath_id = request.session.get('ath_id', None)
                headers = {"content-type": "application/json"}
                payload = {"senderId": ath_id, "recipientPhoneNum": "7877027862", "amount": float("%s" % invoice.total)}
                response = requests.post("http://54.175.166.76:8080/api/makeTransfer",
                                         headers=headers, json=payload)
                data = response.json()
                if data['responseStatus']['status'] == "SUCCESS":
                    invoice.paid = True
                    invoice.save()
                    context["success"] = "This invoice has been successfully paid"
                    return self.render_to_response(context)
                else:
                    context["error"] = "Sorry, Could not make Transfer."
                    return self.render_to_response(context)
            else:
                context["error"] = "Invoice has already been paid"
                return self.render_to_response(context)
        except Invoice.DoesNotExist:
            context['not_found'] = True
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            invoice = Invoice.objects.get(pk=kwargs['pk'])
            context["invoice"] = invoice
            context["items"] = InvoiceItem.objects.filter(invoice=invoice)
            return self.render_to_response(context)
        except Invoice.DoesNotExist:
            context['not_found'] = True
            return self.render_to_response(context)
