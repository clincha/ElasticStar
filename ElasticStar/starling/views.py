from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    context = {
        'oath_link': 'https://oauth-sandbox.starlingbank.com/',
        'client_id': 'BG887EBCs33ZRPzbkfLl',
        'response_type': 'code',
        'state': 'ANGUS12345',
        'redirect_uri': 'https://elasticstar.clinch-home.com/starling/callback',
    }
    return render(request, 'starling/index.html', context)
