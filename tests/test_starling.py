import pytest
import requests_mock

from starling import Starling


@pytest.fixture
def client():
    return Starling("test-token", sandbox=True)


@pytest.fixture
def sandbox_base():
    return "https://api-sandbox.starlingbank.com/api/v2/"


def test_get_accounts(client, sandbox_base):
    accounts_response = {
        "accounts": [
            {
                "accountUid": "abc-123",
                "accountType": "PRIMARY",
                "defaultCategory": "cat-456",
                "currency": "GBP",
                "name": "Personal"
            }
        ]
    }
    with requests_mock.Mocker() as m:
        m.get(sandbox_base + "accounts", json=accounts_response)
        accounts = client.get_accounts()

    assert len(accounts) == 1
    assert accounts[0]["accountUid"] == "abc-123"
    assert accounts[0]["defaultCategory"] == "cat-456"


def test_get_balance(client, sandbox_base):
    balance_response = {
        "effectiveBalance": {"currency": "GBP", "minorUnits": 13887},
        "pendingTransactions": {"currency": "GBP", "minorUnits": 500},
        "totalEffectiveBalance": {"currency": "GBP", "minorUnits": 63887},
    }
    with requests_mock.Mocker() as m:
        m.get(sandbox_base + "accounts/abc-123/balance", json=balance_response)
        balance = client.get_balance("abc-123")

    assert balance["effectiveBalance"]["minorUnits"] == 13887
    assert balance["totalEffectiveBalance"]["minorUnits"] == 63887
    assert balance["pendingTransactions"]["minorUnits"] == 500


def test_get_balance_url(client, sandbox_base):
    with requests_mock.Mocker() as m:
        m.get(sandbox_base + "accounts/uid-xyz/balance", json={})
        client.get_balance("uid-xyz")

    assert m.called
    assert m.last_request.path == "/api/v2/accounts/uid-xyz/balance"


def test_get_transaction_feed(client, sandbox_base):
    next_page = (sandbox_base + "feed/account/abc-123/category/cat-456/"
                 "paginated-transactions?cursor=page-2")
    page_one = {
        "feedItems": [
            {"feedItemUid": "tx-1", "amount": {"currency": "GBP", "minorUnits": 1000}},
        ],
        "links": {"next": next_page},
    }
    page_two = {
        "feedItems": [
            {"feedItemUid": "tx-2", "amount": {"currency": "GBP", "minorUnits": 2000}},
        ],
        "links": {"next": None},
    }
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, [{"json": page_one}, {"json": page_two}])
        items = client.get_transaction_feed("abc-123", "cat-456")

    assert len(items) == 2
    assert items[0]["feedItemUid"] == "tx-1"
    assert items[1]["feedItemUid"] == "tx-2"
    assert len(m.request_history) == 2
    assert "paginated-transactions" in m.request_history[0].url
    assert "category/cat-456" in m.request_history[0].url
    assert "cursor=page-2" in m.request_history[1].url


def test_get_saving_spaces(client, sandbox_base):
    spaces_response = {
        "savingsGoalList": [
            {"name": "Holiday", "totalSaved": {"currency": "GBP", "minorUnits": 50000}}
        ]
    }
    with requests_mock.Mocker() as m:
        m.get(sandbox_base + "account/abc-123/savings-goals", json=spaces_response)
        spaces = client.get_saving_spaces("abc-123")

    assert len(spaces["savingsGoalList"]) == 1
    assert spaces["savingsGoalList"][0]["name"] == "Holiday"
