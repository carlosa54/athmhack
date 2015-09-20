from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^items$',
        views.AddItemView.as_view(),
        name="items"
    ),
    url(
        r'^edititem$',
        views.EditItemView.as_view(),
        name="edititem"
    ),
    url(
        r'dashboard$',
        views.dashboard,
        name="dashboard"
    ),
    url(
        r'dashboard/addInvoice$',
        views.dashboard,
        name="dashAdd"
    ),
]