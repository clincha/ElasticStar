from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    context = {
        'oath_link': 'https://oauth-sandbox.starlingbank.com/',
        'client_id': 'BG887EBCs33ZRPzbkfLl',
        'response_type': 'code',
        'state': 'ANGUS12345',
        'redirect_uri': 'https://clinch-home.com/starling/redirect',
    }
    return render(request, 'starling/index.html', context)
