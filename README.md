# wreck

wreck is a set of scripts dedicated to automate information gathering about targets for penetration testing

wreck uses third-party tools to gather info and generates output in several formats

## Functionality
 - [x] Get subdomains (sublist3r)
 - [ ] Check interesting files on web ports (robots.txt)
 - [ ] Enumerate directories on web
 - [x] Make a screenshot for every target index page
 - [ ] Try to identify technologies used
 - [ ] Crawl web sites
 - [ ] Generate links graph
 - [ ] Generate HTML output

## Installation
```bash
pip install -r requirements.txt
./get-tools.sh
```

## Usage
### Full chain
Run all tools chained together to get report from domain name


Use wreck on domain and subdomains
```bash
python3 ./wreck.py --domain <domain>
```

Use wreck on IP address (subdomain gathering skipped)
```bash
python3 ./wreck.py --ip <ip>
```

Output is saved under `./ouput-<date>/`

### Tools
#### findsubdomains.py
Find subdomains of domain (sublist3r)
```bash
python3 ./findsubdomains.py --domain <domain> --output <output file>
```
#### findwebpages.py
Find HTTP and HTTPS web pages on standart ports of hosts from file
```bash
python3 ./findwebpages.py --hosts <hosts file> --output <output file>
```
#### makescreenshots.py
Take screenshots of every url in file
```bash
python3 ./makescreenshots.py --urls <file with urls> --output <output directory>
```
