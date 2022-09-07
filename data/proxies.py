from itertools import cycle

PROXY_SOURCES = (
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all&simplified=true',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all&anonymity=all&ssl=yes&timeout=2000'
)

def get_proxies(requester) -> cycle:
    return cycle(
        item for item in PROXY_SOURCES 
        for item in requester('GET', item).text.splitlines()
    )