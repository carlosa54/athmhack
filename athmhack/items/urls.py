from django.conf.urls import patterns

from . import views

urlpatterns = patterns(
    # Prefix
    '',
    (
        r'^items$',
        views.ItemView.as_view()
    ),
)