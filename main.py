import os

import tqdm
from ElasticStar.starling.starling import Starling
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

elastic_index = "starling"

if __name__ == '__main__':
    print("Loading environment variables...")
    load_dotenv()
    print("Success!")

    print("Getting transaction history...")
    starling = Starling(os.getenv('PERSONAL_ACCESS_TOKEN'))
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
