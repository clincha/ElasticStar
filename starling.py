from datetime import datetime

import requests

user_agent = "ElasticStar"


class Starling(object):
    def __init__(self, access_token, sandbox=True):
        self.access_token = access_token
        if sandbox:
            self.base_url = "https://api-sandbox.starlingbank.com/api/v2/"
        else:
            self.base_url = "https://api.starlingbank.com/api/v2/"
        self.timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    def get_accounts(self):
        """
        Get an account holder's bank accounts
        :return: A list of the accounts that can be accessed using the access_token.
        """
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'User-Agent': user_agent
        }
        response = requests.get(self.base_url + "accounts", headers=headers)
        response.raise_for_status()
        return response.json()['accounts']

    def get_saving_spaces(self, account_uid):
        """
        Get an account holder's saving spaces
        :param account_uid The unique identifier for this account
        :return: A list of the saving spaces that can be accessed using the access_token in the given account.
        """
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'User-Agent': user_agent
        }
        response = requests.get(self.base_url + "account/" +
                                account_uid + "/savings-goals",
                                headers=headers)
        response.raise_for_status()
        return response.json()

    def get_transaction_feed(self, account_uid, start_date=datetime(1000, 1, 1), end_date=datetime.utcnow()):
        """
        Gets all transactions generated from the given account
        :param account_uid: The unique identifier for this account
        :param start_date: The earliest date to get transactions from (YYYY-MM-DDTHH:MM:SS:000Z)
        :param end_date: The latest date to get transactions from (YYYY-MM-DDTHH:MM:SS:000Z)
        :return: A list of the transactions that can be accessed using the access_token in the given account.
        """
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'User-Agent': user_agent
        }
        response = requests.get(self.base_url + "feed/account/" + account_uid + "/settled-transactions-between?" +
                                "minTransactionTimestamp=" + start_date.strftime(self.timestamp_format) +
                                "&"
                                "maxTransactionTimestamp=" + end_date.strftime(self.timestamp_format),
                                headers=headers
                                )
        response.raise_for_status()
        return response.json()['feedItems']

    @staticmethod
    def generate_elastic_bulk_actions(transaction_feed):
        """
        Converts the given transaction feed into a function that generates actions for interacting with the Elastic API
        :param transaction_feed: A list of the transactions
        :return: Actions for the Elastic API. To be used with the bulk helper function in the Elastic Python API
        """
        for feedItem in transaction_feed:
            document = {
                "_id": feedItem['feedItemUid']
            }
            feedItem.pop('feedItemUid')
            document.update(feedItem)
            yield document

    def get_transaction_attachments(self, account_uid, category_uid, transaction_uid):
        """
        Get the attachments for a specific transaction
        :param account_uid: The unique identifier for this account
        :param category_uid: The unique identifier for this category
        :param transaction_uid: The unique identifier for this transaction
        :return: A list of the attachments that can be accessed using the access_token in the given transaction.
        """
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'User-Agent': user_agent
        }
        response = requests.get(self.base_url + "feed/account/" + account_uid + "/category/" + category_uid +
                                "/" + transaction_uid + "/attachments",
                                headers=headers
                                )
        response.raise_for_status()
        return response.json()['feedItemAttachments']

    def download_transaction_attachment(self, account_uid, category_uid, transaction_uid, attachment_uid,
                                        attachment_type):
        """
        Download a specific attachment for a specific transaction
        :param account_uid: The unique identifier for this account
        :param category_uid: The unique identifier for this category
        :param transaction_uid: The unique identifier for this transaction
        :param attachment_uid: The unique identifier for this attachment
        :param attachment_type: The type of the attachment
        :return: The attachment that can be accessed using the access_token in the given transaction.
        """
        headers = {
            'Authorization': "Bearer " + self.access_token,
            'User-Agent': user_agent
        }
        response = requests.get(self.base_url + "feed/account/" + account_uid + "/category/" + category_uid +
                                "/" + transaction_uid + "/attachments/" + attachment_uid,
                                headers=headers
                                )
        response.raise_for_status()
        Path("attachments").mkdir(parents=True, exist_ok=True)
        if attachment_type == "image":
            attachment_type = "png"
        with open("attachments/" + transaction_uid + "." + attachment_type, "wb") as file:
            file.write(response.content)

        return response.content
