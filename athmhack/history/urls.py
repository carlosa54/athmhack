from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^history$',
        views.HistoryView.as_view(),
        name="history"
    ),
]
