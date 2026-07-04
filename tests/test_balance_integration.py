import os

import pytest

import variables
from starling import Starling

TOKEN_SOURCES = variables.token_sources(os.environ)


def _account_params():
    params = []
    for source_key, token in TOKEN_SOURCES:
        client = Starling(token, sandbox=False)
        for label, account in variables.resolve_labels(client.get_accounts(), source_key):
            params.append(pytest.param((label, client, account), id=label))
    return params


@pytest.mark.skipif(
    not TOKEN_SOURCES,
    reason="No Starling access tokens available"
)
class TestBalanceIntegration:
    @pytest.fixture(params=_account_params() if TOKEN_SOURCES else [])
    def starling_account(self, request):
        return request.param

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
