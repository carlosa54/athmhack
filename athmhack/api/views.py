import requests
from django.shortcuts import render_to_response, redirect

headers = {"content-type": "application/json"}


def loginATHMovil(request):
    payload = {"username": "gabriel", "password": "gabriel"}
    response = requests.post("http://54.175.166.76:8080/api/login", json=payload)
    return render_to_response('api.html', {"status": response.status_code,
                                           "data": response.json})


def make_transaction(request):
    payload = {"id"}

