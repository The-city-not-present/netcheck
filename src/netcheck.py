

from . network_ping import get_status as get_ping_status
from . network_nslookup import get_status as get_nslookup_status
from . network_http_request import get_status as get_httprequest_status

PING_TARGETS="1.1.1.1 8.8.8.8"
DNS_TARGET="google.com mail.ru ru.wikipedia.org youtube.com praha.eu thelapod.com portal.rozhlas.cz cvut.cz ixbt.com omgvpn.com"
HTTP_TARGETS="https://www.google.com/generate_204 https://cloudflare.com/cdn-cgi/trace http://example.com https://omgvpn.com/ip"



def probe_statuses():
    results = []
    for target in PING_TARGETS.split():
        result = get_ping_status(target)
        results.append(result)

    for target in DNS_TARGET.split():
        result = get_nslookup_status(target)
        results.append(result)

    for target in HTTP_TARGETS.split():
        result = get_httprequest_status(target)
        results.append(result)

    return results
