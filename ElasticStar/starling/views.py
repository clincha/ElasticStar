import os

import requests
import tqdm
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from ElasticStar.starling.starling import Starling

client_id = 'BG887EBCs33ZRPzbkfLl'
redirect_uri = 'https://elasticstar.clinch-home.com/starling/callback'

elastic_index = 'elasticstar'


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

    access_token_request_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(
        url='https://api-sandbox.starlingbank.com/oauth/access-token',
        data=access_token_request_data
    )

    if response.status_code == 200:
        starling = Starling(response.json()['access_token'])
        main_account = starling.get_accounts()[0]['accountUid']
        transactions = starling.get_transaction_feed(main_account)
        print("Success!")

        print("Adding transactions to Elastic...")
        elastic = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=("elastic", os.getenv("ELASTIC_CLOUD_PASSWORD"))
        )
        progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions['feedItems']))
        for ok, action in streaming_bulk(
                client=elastic,
                index=elastic_index,
                actions=starling.generate_elastic_bulk_actions(transactions)
        ):
            progress.update(1)

        return JsonResponse(response.json())
    else:
        return HttpResponseServerError(str(response.status_code) + ' - ' + response.reason)
