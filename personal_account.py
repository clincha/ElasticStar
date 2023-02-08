import os

import tqdm
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from ElasticStar.starling.Starling import Starling

if __name__ == '__main__':
    load_dotenv()

    accounts = [
        {"type": "personal"},
        {"type": "business"}
    ]

    for account in accounts:
        print("Getting transaction history...")
        print('{account_type}_ACCESS_TOKEN'.format(account_type=account['type'].capitalize()))
        starling = Starling(os.getenv(
            '{account_type}_ACCESS_TOKEN'.format(account_type=account['type'].capitalize())),
            sandbox=False)
        main_account = starling.get_accounts()[0]['accountUid']
        transactions = starling.get_transaction_feed(main_account)
        print("Success!")

        print("Adding transactions to Elastic...")
        elastic = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=("elastic", os.getenv("ELASTIC_CLOUD_PASSWORD"))
        )
        elastic_index = "CLINCHA_STARLING_{account_type}".format(account_type=account['type'].capitalize())
        elastic.indices.create(index=elastic_index, ignore=400)  # ignore 400 (IndexAlreadyExistsException)
        progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions['feedItems']))
        for ok, action in streaming_bulk(
                client=elastic,
                index=elastic_index,
                actions=starling.generate_elastic_bulk_actions(transactions)
        ):
            progress.update(1)
