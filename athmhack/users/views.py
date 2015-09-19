from django.views.generic import TemplateView
from django.contrib.auth import logout

from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    return redirect("/")


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super(HomeView, self).get_context_data(**kwargs)


class LoginView(TemplateView):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            return redirect("/dashboard")
        return self.render_to_response(context)
