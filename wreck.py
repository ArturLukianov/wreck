#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import time
import colorama
from makescreenshots import make_screenshots
from findwebpages import find_web_pages
from findsubdomains import find_subdomains
from generatehtmlreport import generate_html_report


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



if __name__ == "__main__":
    targets = set()
    target_urls = set()
    screenshots = dict()

    banner()
    
    parser = argparse.ArgumentParser(description='Automated information gathering')
    target_me_group = parser.add_mutually_exclusive_group(required=True)
    target_me_group.add_argument('--domain', dest='domain')
    target_me_group.add_argument('--ip', dest='ip')
    parser.add_argument('--subbrute', dest='subbrute', action='store_true', help='Preform subdomain bruteforce')
    args = parser.parse_args()

    subbrute = args.subbrute

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
        targets |= set(find_subdomains(args.domain, subdomains_file, subbrute))
    elif 'ip' in args:
        print('%s[!] %sTarget: %s%s%s' % (B, W, Y, args.ip, W))
        targets.add(args.ip)

    print('%s[+] %sTarget discovery finished' % (G, W))
    print('%s[!] %sDetecting web sites' % (B, W))

    target_urls = find_web_pages(targets, True)
    
    for i, url in enumerate(target_urls):
        if i == 0:
            print('%s[+] %sFound: %s%s%s' % (G, W, Y, url, W))
        else:
            print('           %s%s%s' % (Y, url, W))

    print('%s[!] %sTaking screenshots of index pages' % (B, W))

    screenshots_directory = os.path.join(working_directory, 'screenshots')
    
    print('%s[!] %sScreenshots will be saved in %s%s%s' % (B, W, Y, screenshots_directory, W))
    
    make_screenshots(target_urls, screenshots_directory)

    print('%s[+] %sScreenshots saved' % (G, W))

    print('%s[!] %sGenerating HTML report' % (B, W))
    
    html_dir = os.path.join(working_directory, 'html')
    print('%s[!] %sHTML report will be saved in %s%s%s' % (B, W, Y, html_dir, W))
    generate_html_report('Wreck report', html_dir, target_urls)
    print('%s[+] %sFinished!' % (G, W))

