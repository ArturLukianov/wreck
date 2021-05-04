#!/usr/bin/env python3
import sublist3r
import argparse


def find_subdomains(domain, output_file, enable_bruteforce=False):
    subdomains = sublist3r.main(domain, 12, output_file, ports=None, verbose=False, enable_bruteforce=enable_bruteforce, engines=None, silent=False)
    return subdomains


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find subdomains")
    parser.add_argument("--domain", dest="domain", required=True)
    parser.add_argument("--output", dest="output", default="subdomains.txt")
    parser.add_argument("--subbrute", dest="subbrute", action="store_true", help="Preform subdomain bruteforce search")

    args = parser.parse_args()
    find_subdomains(args.domain, args.output, args.subbrute)
    
