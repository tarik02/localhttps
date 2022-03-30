import re

domain_regex = re.compile(r'^(?:https?://)?([^/]+)')

def normalize_domain(domain: str) -> str:
    match = domain_regex.match(domain)
    if match is not None:
        return match.group(1)
    else:
        return domain
