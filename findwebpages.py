#!/usr/bin/env python3
import requests
import argparse


def find_web_pages(targets, verbose=False):
    target_urls = set()
    for address in targets:
        if verbose:
            print('[!] Checking %s' % address)
        http_url = 'http://' + address
        try:
            response = requests.get(http_url, allow_redirects=False, timeout=3)
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        
        if response.status_code == 301:
            target_urls.add(response.headers['Location'])
        elif response.status_code == 200:
            target_urls.add(http_url)

        https_url = 'https://' + address
        try:
            response = requests.get(https_url, allow_redirects=False, timeout=3)
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        
        if response.status_code == 301:
            target_urls.add(response.headers['Location'])
        elif response.status_code == 200:
            target_urls.add(https_url)

    return target_urls



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find web pages on hosts")
    parser.add_argument("--hosts", dest="hosts", required=True)
    parser.add_argument("--verbose", dest="verbose", action="store_true")
    parser.add_argument("--output", dest="output", default="pages.txt")


    args = parser.parse_args()
    with open(args.hosts) as hosts_file:
        pages = find_web_pages([i.strip() for i in hosts_file.readlines()], verbose=args.verbose)
        with open(args.output, 'w+') as output_file:
            output_file.write('\n'.join(pages))
    
