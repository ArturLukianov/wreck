# wreck

wreck is a set of scripts dedicated to automated information gathering about targets for penetration testing

wreck uses third-party tools to gather info and generates output in several formats

## Functionality
 - [ ] Get subdomains (sublist3r)
 - [ ] Check interesting files on web ports (robots.txt)
 - [ ] Enumerate directories on web
 - [ ] Make a screenshot for every web port main page
 - [ ] Try to identify technologies used
 - [ ] Generate HTML output

## Installation
```bash
pip install -r requirements.txt
./get-tools.sh
```

## Usage

Use wreck on domain and subdomains
```bash
python3 ./wreck.py --domain <domain>
```

Use wreck on IP address (subdomain gathering skipped)
```bash
python3 ./wreck.py --ip <ip>
```

Output is saved under `./ouput-<date>/`
