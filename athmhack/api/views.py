from django.shortcuts import render

import requests
import json


def create_user_athmovil(request):
    headers = {'content-type': 'application/json'}
    # payload = {'token': "hackhackhackhackhackhackhack"}
    payload = {""}