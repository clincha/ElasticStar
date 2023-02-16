import os

import elasticsearch
import tqdm
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from starling import Starling

if __name__ == '__main__':
    load_dotenv()
    accounts = ['PERSONAL', 'BUSINESS', 'JOINT']

    for account in accounts:
        access_token = '{account_type}_ACCESS_TOKEN'.format(account_type=account)
        if access_token not in os.environ:
            continue

        print("Getting transaction history for account type: {account_type}".format(account_type=account))
        starling = Starling(
            os.getenv(access_token),
            sandbox=False)
        main_account = starling.get_accounts()[0]['accountUid']
        transactions = starling.get_transaction_feed(main_account)

        elastic = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
        )
        elastic_index = "CLINCHA_STARLING_{account_type}".format(account_type=account).lower()
        try:
            elastic.indices.create(index=elastic_index)
            print("Creating index...")
        except elasticsearch.BadRequestError as error:
            if error.message == 'resource_already_exists_exception':
                pass
            else:
                raise error

        progress = tqdm.tqdm(unit="documents", total=sum(1 for _ in transactions['feedItems']))
        print("Adding transactions to Elastic...")
        for ok, action in streaming_bulk(
                client=elastic,
                index=elastic_index,
                actions=starling.generate_elastic_bulk_actions(transactions)
        ):
            progress.update(1)
