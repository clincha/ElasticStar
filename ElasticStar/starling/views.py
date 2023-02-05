import os

import requests
import tqdm
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from .Starling import Starling

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
        elastic = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=("elastic", os.getenv("ELASTIC_CLOUD_PASSWORD"))
        )

        starling = Starling(response.json()['access_token'])
        try:
            for account in starling.get_accounts():
                account_index = elastic_index + ":" + account['accountUid']
                elastic.indices.create(index=account_index)
                transactions = starling.get_transaction_feed(account['accountUid'])

                progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions['feedItems']))
                for ok, action in streaming_bulk(
                        client=elastic,
                        index=account_index,
                        actions=starling.generate_elastic_bulk_actions(transactions)
                ):
                    progress.update(1)
        except requests.exceptions.HTTPError as error:
            return HttpResponseServerError(str(error))

        return HttpResponse("Completed!")
    else:
        return HttpResponseServerError(str(response.status_code) + ' - ' + response.reason)
