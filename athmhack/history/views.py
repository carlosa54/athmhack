from django.views.generic import TemplateView
from django.shortcuts import redirect

import requests


class HistoryView(TemplateView):
    template_name = "dashboard/history.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login')
        context = self.get_context_data(**kwargs)
        ath_id = request.session.get('ath_id', None)
        headers = {"content-type": "application/json"}

        payload = {"id": ath_id}
        response = requests.post("http://54.175.166.76:8080/api/transferHistory/inbound",
                                 headers=headers, json=payload)
        data = response.json()

        if data['responseStatus']['status'] == "SUCCESS":
            payments_sent = data['transferList']
            context["payments_sent"] = payments_sent

        ath_id = request.session.get('ath_id', None)
        payload = {"id": ath_id}
        response = requests.post("http://54.175.166.76:8080/api/transferHistory/outbound",
                                 headers=headers, json=payload)
        #data = response.json()
        #print data
        #if data['responseStatus']['status'] == "SUCCESS":
        #    payments_received = data['transferList']
        #    context["payments_received"] = payments_received

        return self.render_to_response(context)
