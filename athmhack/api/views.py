import requests
from django.shortcuts import render_to_response, redirect

headers = {"content-type": "application/json"}


def loginATHMovil(request):
    payload = {"username": "gabriel", "password": "gabriel"}
    response = requests.post("http://54.175.166.76:8080/api/login", json=payload)
    return render_to_response('api.html', {"status": response.status_code,
                                           "data": response.json})


def make_transaction(request):
    if not request.user.is_authenticated():
        return redirect("/login")
    ath_id = request.session.get('ath_id', None)
    payload = {"senderId": ath_id, "recipientPhoneNum": "7877027862", "amount": 80}
    response = requests.post("http://54.175.166.76:8080/api/makeTransfer",
                             headers=headers, json=payload)
    return render_to_response("api.html", {"status": response.status_code,
                                           "data": response.json})


def history_transaction_outgoing(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    ath_id = request.session.get('ath_id', None)
    payload = {"id": ath_id}
    response = requests.post("http://54.175.166.76:8080/api/transferHistory/outbound",
                             headers=headers, json=payload)
    return render_to_response("api.html", {"status": response.status_code,
                                           "data": response.json})


def history_transaction_inbound(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    ath_id = request.session.get('ath_id', None)
    print ath_id
    payload = {"id": ath_id}
    response = requests.post("http://54.175.166.76:8080/api/transferHistory/inbound",
                             headers=headers, json=payload)
    return render_to_response("api.html", {"status": response.status_code,
                                           "data": response.json})


def send_sms_text(request):
    payload = {"number": "7877027862", "message": "A test https://cashin.herokuapp.com"}
    response = requests.post("http://textbelt.com/text", json=payload)
    return render_to_response("api.html", {"status": response.status_code,
                                           "data": response.json})
