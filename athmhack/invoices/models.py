from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template import loader

from .constants import INVOICE_STATUS
from ..utils.models import BaseModel
from ..users.models import User
from ..items.models import Item


# Create your models here.
class Invoice(BaseModel):
    biller = models.ForeignKey(User, related_name="biller")
    client = models.ForeignKey(User, related_name="client")
    items = models.ManyToManyField(Item, through='InvoiceItem')
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return "biller: %s client: %s" % (self.biller, self.client)

    @property
    def total(self):
        invoice_items = InvoiceItem.objects.filter(invoice=self.id)
        total = 0
        for invoice in invoice_items:
            total += invoice.subtotal
        return total

    def send_invoice(self):
        context = self.client.get_email_context()
        context["url"] = "invoices/%d" % self.id
        self.client.email_user(
            subject="Invoice #%d" % self.id,
            message=loader.render_to_string(
                "email/invoice_sent.html",
                context)
        )


class InvoiceItem(BaseModel):
    item = models.ForeignKey(Item)
    invoice = models.ForeignKey(Invoice)
    quantity = models.IntegerField(validators= [MinValueValidator(0), MaxValueValidator(100)])

    @property
    def subtotal(self):
        return self.item.price * self.quantity