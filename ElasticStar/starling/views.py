import os

import requests
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from dotenv import load_dotenv, find_dotenv

client_id = 'BG887EBCs33ZRPzbkfLl'
redirect_uri = 'https://elasticstar.clinch-home.com/starling/callback'


def index(request):
    context = {
        'oath_link': 'https://oauth-sandbox.starlingbank.com/',
        'client_id': client_id,
        'response_type': 'code',
        'state': 'ANGUS12345',
        'redirect_uri': redirect_uri,
    }
    return render(request, 'starling/index.html', context)


def callback(request):
    load_dotenv(find_dotenv())
    client_secret = os.environ['STARLING_CLIENT_SECRET']

    code = request.GET.get('code')
    state = request.GET.get('state')

    if state != 'ANGUS12345':
        return HttpResponseServerError

    headers = {
        'application': 'x-www-form-urlencoded'
    }

    parameters = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.get(
        url='https://api-sandbox.starlingbank.com/oauth/access-token',
        headers=headers,
        params=parameters
    )

    print(response.json())
