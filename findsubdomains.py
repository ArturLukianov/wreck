#!/usr/bin/env python3
import sublist3r

def find_subdomains(domain, output_file, enable_bruteforce=False):
    subdomains = sublist3r.main(domain, 12, output_file, ports=None, verbose=False, enable_bruteforce=enable_bruteforce, engines=None, silent=False)
    return subdomains
