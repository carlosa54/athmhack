from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.HomeView.as_view(),
        name="home"
    ),
    url(
        r'^register$',
        views.RegisterView.as_view(),
        name="register"
    ),
    url(
        r'^login$',
        views.LoginView.as_view(),
        name="login"
    ),
]