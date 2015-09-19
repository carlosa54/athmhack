from django.conf.urls import patterns

from . import views

urlpatterns = patterns(
    # Prefix
    '',
    (
        r'^$',
        views.HomeView.as_view()
    ),
)