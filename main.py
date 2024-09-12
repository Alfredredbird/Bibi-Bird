import requests
import os
from bs4 import BeautifulSoup
import argparse
from modules.scans import *
from modules.mods import *

# Variables á••( á› )á•—
url = ""
wordlistpath = ""
payload = 0
delay = 3

parser = argparse.ArgumentParser(
                    prog='BiBi',
                    description='Scans websites for vulnerabilities',
                    epilog='Hello from Bibi')

parser.add_argument('-b', '--brute', action='store_true')
parser.add_argument('-u', '--url')
parser.add_argument('-l', '--lengths', type=int, nargs=2, help='Minimum and maximum length for subdomain brute-forcing')
parser.add_argument('-w', '--wordlist')
parser.add_argument('-i', '--inject', action='store_true', help='SQL Injection Mode')
parser.add_argument('-p', '--payload', type=int)
parser.add_argument('-d', '--delay', type=int)
parser.add_argument('-x', '--xss', type=int)

arg = parser.parse_args()

# main functions on start up

chrome_options = Options()

# chrome_options.add_argument("--headless")   
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument( "--log-level=3") 
driver = webdriver.Chrome(options=chrome_options)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    "DNT": "1"  
}

if arg.url is None:
    url = input("Target: ")
else:
    url = arg.url

if arg.payload:
 payload = arg.payload

if arg.delay:
    delay = arg.delay
if arg.xss:
   mode = arg.xss


if arg.wordlist:
 if arg.wordlist is None:
    wordlistpath = input("Wordlist: ")
 else:
    wordlistpath = arg.wordlist

try:
 response = requests.get(str(url), headers=headers)
except Exception as e:
   print("================================================")
   print(f"Error: {e}")
   print("================================================")
   exit(1)

logo(url,response)

if response.status_code >= 400:
   print("Error")
else:
   
   if arg.brute:
    # brute(url,driver,response)
    subdomain(url,driver, "dict/sec.txt")
   if arg.inject:
       inject(url,driver,response,wordlistpath,payload,delay)
   if arg.xss:
       xssScan(driver,url,mode)
        
print("⟪                                               ⟫")
print("⟪±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±⟫")