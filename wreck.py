#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import time
import colorama
import sublist3r
import requests
from screenshot import Screenshot
from PyQt5.QtWidgets import QApplication


# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console , colorama
        win_unicode_console.enable()
        colorama.init()
        #Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used")
        G = Y = B = R = W = G = Y = B = R = W = ''
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white


def no_color():
    global G, Y, B, R, W
    G = Y = B = R = W = ''


def banner():
    print("""%s
                ┬ ┬┬─┐┌─┐┌─┐┬┌─
                │││├┬┘├┤ │  ├┴┐
                └┴┘┴└─└─┘└─┘┴ ┴%s
               by @ArturLukianov%s
    """ % (G, R, W))
    


def prepare_working_directory(working_directory):
    os.mkdir(working_directory)

    
def find_subdomains(domain, output_file, enable_bruteforce=False):
    subdomains = sublist3r.main(domain, 12, output_file, ports=None, verbose=False, enable_bruteforce=enable_bruteforce, engines=None, silent=True)
    return subdomains


if __name__ == "__main__":
    targets = set()
    target_urls = set()
    screenshots = dict()

    banner()
    
    parser = argparse.ArgumentParser(description='Automated information gathering')
    target_me_group = parser.add_mutually_exclusive_group(required=True)
    target_me_group.add_argument('--domain', dest='domain')
    target_me_group.add_argument('--ip', dest='ip')
    args = parser.parse_args()

    working_directory = os.path.join(os.path.abspath(os.getcwd()),
                                     'output-%s' % (datetime.today().strftime('%Y-%m-%d-%s'),))

    print('%s[+]%s Created working directory: %s%s%s' %
          (G, W, Y, working_directory, W))

    prepare_working_directory(working_directory)

    if 'domain' in args:
        print('%s[!] %sPrimary target: %s%s%s' % (B, W, Y, args.domain, W))
        targets.add(args.domain)
        
        print('%s[!] %sLooking for subdomains...' % (B, W))
        subdomains_file = os.path.join(working_directory,
                                       'subdomains-sublist3r.txt')
        targets |= set(find_subdomains(args.domain, subdomains_file))
    else:
        print('%s[!] %sTarget: %s%s%s' % (B, W, Y, args.ip, W))
        targets.add(args.ip)

    print('%s[+] %sTarget discovery finished' % (G, W))
    print('%s[!] %sDetecting web sites' % (B, W))
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

    for i, url in enumerate(target_urls):
        if i == 0:
            print('%s[+] %sFound: %s%s%s' % (G, W, Y, url, W))
        else:
            print('           %s%s%s' % (Y, url, W))

    print('%s[!] %sTaking screenshots of index pages' % (B, W))

    url_file_pairs = []
    
    for url in target_urls:
        output_file = os.path.join(working_directory,
                                   'screenshot-' +
                                   ''.join([i for i in url if i.isalpha()]) + '.png')
        url_file_pairs.append((url, output_file))
        
    app = QApplication([])
    s = Screenshot()
    s.app = app    
    s.capture(url_file_pairs)

    app.exec_()

    print('%s[+] %sScreenshots saved' % (G, W))



