from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^transfer$',
        views.make_transaction,
        name="transfer"
    ),
    url(
        r'^transactions/inbound',
        views.history_transaction_inbound,
        name="inbound"
    ),
    url(
        r'^transactions/outbound',
        views.history_transaction_outgoing,
        name="outbound"
    ),
    url(
        r'^sms',
        views.send_sms_text,
        name="sms"
    ),
]
