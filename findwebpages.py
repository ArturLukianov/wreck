#!/usr/bin/env python3
import requests


def find_web_pages(targets):
    target_urls = set()
    for address in targets:
        http_url = 'http://' + address
        try:
            response = requests.get(http_url, allow_redirects=False)
        except requests.exceptions.ConnectionError:
            continue
        
        if response.status_code == 301:
            target_urls.add(response.headers['Location'])
        elif response.status_code == 200:
            target_urls.add(http_url)

        https_url = 'https://' + address
        try:
            response = requests.get(https_url, allow_redirects=False)
        except requests.exceptions.ConnectionError:
            continue
        
        if response.status_code == 301:
            target_urls.add(response.headers['Location'])
        elif response.status_code == 200:
            target_urls.add(https_url)
    return target_urls
