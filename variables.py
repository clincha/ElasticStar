import re

index_prepend = "CLINCHA_STARLING_"
accounts = ['PERSONAL', 'BUSINESS', 'JOINT']
single_token_key = 'STARLING_ACCESS_TOKEN'


def _slugify(value):
    slug = re.sub(r'[^a-z0-9]+', '-', str(value).lower()).strip('-')
    return slug or 'account'


def _account_slug(account):
    return _slugify(account.get('name') or account.get('accountType') or account.get('accountUid'))


def token_sources(environ):
    """Return (source_key, token) pairs for every configured token that is present.

    The per-type keys (PERSONAL/BUSINESS/JOINT) are retained for backward
    compatibility; single_token_key exposes every account linked to one
    developer token and carries a None source_key.
    """
    sources = [(key, environ.get(f'{key}_ACCESS_TOKEN')) for key in accounts]
    sources.append((None, environ.get(single_token_key)))
    return [(key, token) for key, token in sources if token]


def resolve_labels(account_list, source_key=None):
    """Map every account a token exposes to a stable, unique label.

    A legacy per-type token holding a single account keeps its env-key label so
    existing indices/sheets are reused. Any other case derives the label from
    the account itself, disambiguating collisions with the accountUid.
    """
    if source_key is not None and len(account_list) == 1:
        return [(source_key.lower(), account_list[0])]

    labels = []
    used = set()
    for account in account_list:
        base = _account_slug(account)
        label = base
        if label in used:
            suffix = str(account.get('accountUid', ''))[:8]
            label = f"{base}-{suffix}" if suffix else base
        used.add(label)
        labels.append((label, account))
    return labels
