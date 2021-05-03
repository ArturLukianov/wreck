#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import time
import colorama
import sublist3r


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
    targets = []

    banner()
    
    parser = argparse.ArgumentParser(description='Automated information gathering')
    target_me_group = parser.add_mutually_exclusive_group(required=True)
    target_me_group.add_argument('--domain', dest='domain')
    target_me_group.add_argument('--ip', dest='ip')
    args = parser.parse_args()

    working_directory = os.path.join(os.path.abspath(os.getcwd()),
                                     'output-%s' % (datetime.today().strftime('%Y-%m-%d-%s'),))

    print('%s[+]%s Created working directory: %s%s%s' %
          (G, W, Y, working_directory, Y))

    prepare_working_directory(working_directory)

    if 'domain' in args:
        print('%s[!] %sPrimary target: %s%s%s' % (B, W, Y, args.domain, W))
        targets.append(args.domain)
        
        print('%s[!] %sLooking for subdomains...' % (B, W))
        subdomains_file = os.path.join(working_directory,
                                       'subdomains-sublist3r.txt')
        targets += find_subdomains(args.domain, subdomains_file)
    else:
        print('%s[!] %sTarget: %s%s%s' % (B, W, Y, args.ip, W))
        targets.append(args.ip)
