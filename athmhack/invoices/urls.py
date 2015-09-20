from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^invoices$',
        views.AddInvoiceView.as_view(),
        name="invoices"
    ),
    url(
        r'^invoices/(?P<pk>[0-9]+)$',
        views.RetrieveInvoiceView.as_view(),
        name="invoice"
    ),
]
