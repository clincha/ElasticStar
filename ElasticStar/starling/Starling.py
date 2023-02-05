from datetime import datetime
import requests


class Starling(object):
    base_url = "https://api.starlingbank.com/api/v2/"
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, personal_access_token):
        self.personal_access_token = personal_access_token

    def get_accounts(self):
        """
        Get an account holder's bank accounts
        :return: An array containing all the users accounts. Account object keys:
            - accountUid
            - accountType
            - defaultCategory
            - currency
            - createdAt
            - name
        """
        headers = {
            'Authorization': "Bearer " + self.personal_access_token
        }
        response = requests.get("https://api.starlingbank.com/api/v2/accounts", headers=headers)
        if response.status_code == 200:
            return response.json()['accounts']
        else:
            raise ValueError('Personal access token is likely incorrect - ' + self.personal_access_token)

    def get_saving_spaces(self, account_uid):
        """
        Gets all the saving spaces associated with the given personal access token
        :return: A list of saving spaces which in turn are a list of strings
        """
        headers = {
            'Authorization': "Bearer " + self.personal_access_token
        }
        response = requests.get(
            "https://api.starlingbank.com/api/v2/account/" + account_uid + "/savings-goals",
            headers=headers)
        return response.json()

    def get_transaction_feed(self, account_uid):
        headers = {
            'Authorization': "Bearer " + self.personal_access_token
        }
        response = requests.get(self.base_url + "feed/account/" + account_uid + "/settled-transactions-between?" +
                                "minTransactionTimestamp=" + "1000-01-01T00:00:00Z" +
                                "&"
                                "maxTransactionTimestamp=" + datetime.utcnow().strftime(self.timestamp_format),
                                headers=headers
                                )
        return response.json()

    @staticmethod
    def generate_elastic_bulk_actions(transaction_feed):
        for feedItem in transaction_feed['feedItems']:
            document = {
                "_id": feedItem['feedItemUid']
            }
            feedItem.pop('feedItemUid')
            document.update(feedItem)
            yield document
