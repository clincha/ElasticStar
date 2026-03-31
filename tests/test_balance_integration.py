import os

import pytest

from starling import Starling

ACCOUNTS = {
    "PERSONAL": os.environ.get("PERSONAL_ACCESS_TOKEN"),
    "BUSINESS": os.environ.get("BUSINESS_ACCESS_TOKEN"),
    "JOINT": os.environ.get("JOINT_ACCESS_TOKEN"),
}


@pytest.mark.skipif(
    not any(ACCOUNTS.values()),
    reason="No Starling access tokens available"
)
class TestBalanceIntegration:
    @pytest.fixture(params=[
        name for name, token in ACCOUNTS.items() if token
    ])
    def starling_account(self, request):
        name = request.param
        token = ACCOUNTS[name]
        client = Starling(token, sandbox=False)
        account = client.get_accounts()[0]
        return name, client, account

    def test_balance_endpoint_returns_expected_fields(self, starling_account):
        name, client, account = starling_account
        balance = client.get_balance(account["accountUid"])

        assert "effectiveBalance" in balance
        assert "currency" in balance["effectiveBalance"]
        assert "minorUnits" in balance["effectiveBalance"]
        assert "totalEffectiveBalance" in balance
        assert "pendingTransactions" in balance

    def test_balance_matches_transactions_within_pending_tolerance(self, starling_account):
        name, client, account = starling_account
        account_uid = account["accountUid"]

        balance = client.get_balance(account_uid)
        effective = balance["effectiveBalance"]["minorUnits"]
        pending = balance["pendingTransactions"]["minorUnits"]

        transactions = client.get_transaction_feed(account_uid)
        tx_sum = 0
        for tx in transactions:
            minor = tx["amount"]["minorUnits"]
            if tx["direction"] == "IN":
                tx_sum += minor
            else:
                tx_sum -= minor

        spaces = client.get_saving_spaces(account_uid)
        spaces_total = sum(
            s["totalSaved"]["minorUnits"]
            for s in spaces.get("savingsGoalList", [])
        )

        computed_balance = tx_sum - spaces_total
        difference = abs(effective - computed_balance)

        assert difference <= abs(pending) + 100, (
            f"{name}: effective={effective}, computed={computed_balance}, "
            f"pending={pending}, difference={difference}"
        )
