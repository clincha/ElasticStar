import os

import elasticsearch
import tqdm
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import variables

from starling import Starling

if __name__ == '__main__':
    load_dotenv()

    elastic = Elasticsearch(
        hosts=[os.getenv('ELASTIC_HOST')],
        basic_auth=(os.getenv('ELASTIC_USERNAME'), os.getenv('ELASTIC_PASSWORD')),
    )

    for source_key, token in variables.token_sources(os.environ):
        starling = Starling(token, sandbox=False)

        for label, account in variables.resolve_labels(starling.get_accounts(), source_key):
            print(f"Getting transaction history for account: {label}")
            transactions = starling.get_transaction_feed(account['accountUid'])

            elastic_index = (variables.index_prepend + label).lower()
            try:
                print("Creating index...")
                elastic.indices.create(index=elastic_index)
            except elasticsearch.BadRequestError as error:
                if error.message != 'resource_already_exists_exception':
                    raise error

            print("Adding transactions to Elastic...")
            progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions))
            for ok, action in streaming_bulk(
                    client=elastic,
                    index=elastic_index,
                    actions=starling.generate_elastic_bulk_actions(transactions)
            ):
                progress.update(1)
            progress.close()
