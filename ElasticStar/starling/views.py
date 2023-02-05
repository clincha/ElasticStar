import os

import requests
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import render
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
        return HttpResponseServerError('Incorrect state')

    parameters = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(
        url='https://api-sandbox.starlingbank.com/oauth/access-token',
        params=parameters
    )

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return HttpResponseServerError(str(response.status_code) + ' - ' + response.reason)
