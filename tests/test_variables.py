import variables


def test_token_sources_includes_present_tokens_only():
    environ = {
        "PERSONAL_ACCESS_TOKEN": "p",
        "STARLING_ACCESS_TOKEN": "s",
    }
    sources = variables.token_sources(environ)

    assert ("PERSONAL", "p") in sources
    assert (None, "s") in sources
    assert all(key != "BUSINESS" for key, _ in sources)


def test_legacy_single_account_keeps_env_key_label():
    accounts = [{"accountUid": "abc-123", "name": "Angus Personal"}]
    labels = variables.resolve_labels(accounts, source_key="PERSONAL")

    assert labels == [("personal", accounts[0])]


def test_single_token_yields_a_label_per_account():
    accounts = [
        {"accountUid": "abc-123", "name": "Personal"},
        {"accountUid": "def-456", "name": "Joint"},
        {"accountUid": "ghi-789", "name": "Business"},
    ]
    labels = variables.resolve_labels(accounts)

    assert [label for label, _ in labels] == ["personal", "joint", "business"]
    assert len(labels) == len(accounts)


def test_colliding_names_are_disambiguated_by_uid():
    accounts = [
        {"accountUid": "abc-123", "name": "Savings"},
        {"accountUid": "def-456", "name": "Savings"},
    ]
    labels = [label for label, _ in variables.resolve_labels(accounts)]

    assert labels[0] == "savings"
    assert labels[1] == "savings-def-456"
    assert len(set(labels)) == 2


def test_label_falls_back_to_type_then_uid():
    accounts = [
        {"accountUid": "abc-123", "accountType": "ADDITIONAL"},
        {"accountUid": "def-456"},
    ]
    labels = [label for label, _ in variables.resolve_labels(accounts)]

    assert labels == ["additional", "def-456"]
