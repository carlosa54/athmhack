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
    url(
        r'^logout$',
        views.user_logout,
        name="logout"
    ),
    url(
        r'^dashboard$',
        views.DashBoardView.as_view(),
        name="dashboard"
    ),
]