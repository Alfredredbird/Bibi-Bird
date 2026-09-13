import requests
import os
import argparse
import json
from datetime import datetime
from modules.scans import *
from modules.mods import *
from modules.bireq import *
from urllib.parse import urlparse
# Variables á••( á› )á•—
url = ""
wordlistpath = ""
payload = 0
delay = 3
mode = 1

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
parser.add_argument('-r', '--repeat', type=int)
parser.add_argument('-c', '--csrf', type=str, help='Cross Site Request Forgery Mode')
parser.add_argument('--sql-detect', action='store_true', help='Passive SQL error detection mode')
parser.add_argument('--report', type=str, help='Write scan summary report to a JSON file')

arg = parser.parse_args()


def normalize_url(raw_url):
    """Ensure URL has a scheme and is not empty."""
    if not raw_url:
        return ""
    parsed = urlparse(raw_url)
    if not parsed.scheme:
        return f"http://{raw_url}"
    return raw_url


def write_report(path, report_data):
    report_data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    try:
         parent_dir = os.path.dirname(path)
         if parent_dir:
             os.makedirs(parent_dir, exist_ok=True)
         with open(path, "w") as report_file:
             json.dump(report_data, report_file, indent=2)
     except OSError as exc:
         print(f"Failed to write report to '{path}': {exc}")

# main functions on start up

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

if arg.url is None and arg.csrf is None:
    url = normalize_url(input("Target: ").strip())
else:
    url = normalize_url(arg.url)

if arg.payload:
    payload = arg.payload

if arg.delay:
    delay = arg.delay
if arg.xss:
    mode = arg.xss


if arg.wordlist:
    wordlistpath = arg.wordlist

selected_modes = [arg.brute, arg.inject, bool(arg.xss), bool(arg.csrf), arg.sql_detect]
if not any(selected_modes):
    parser.print_help()
    exit(0)

try:
    if url:
        response = requests.get(str(url), headers=headers, timeout=15)
    else:
        print("================================================")
        print("Error: Missing target URL")
        print("================================================")
        exit(1)
except Exception as e:
    print("================================================")
    print(f"Error: {e}")
    print("================================================")
    exit(1)

logo(url,response)

scan_report = {
    "target": url,
    "http_status": response.status_code,
    "modes": {
        "brute": bool(arg.brute),
        "inject": bool(arg.inject),
        "xss": bool(arg.xss),
        "csrf": bool(arg.csrf),
        "sql_detect": bool(arg.sql_detect)
    },
    "results": {}
}

driver = None
requires_driver = arg.brute or arg.inject or bool(arg.xss)

if requires_driver:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)

if response.status_code >= 400:
   print("Error")
else:
    try:
        if arg.brute and driver is not None:
            findings = subdomain(url, driver, "dict/sec.txt")
            scan_report["results"]["brute"] = {
                "discoveries": findings,
                "count": len(findings)
            }
        if arg.inject and driver is not None:
            inject_result = inject(url, driver, response, wordlistpath, payload, delay)
            scan_report["results"]["inject"] = inject_result
        if arg.xss and driver is not None:
            xss_result = xssScan(driver, url, mode)
            scan_report["results"]["xss"] = xss_result
        if arg.sql_detect:
            detect_result = detect_sql_errors(url, headers)
            scan_report["results"]["sql_detect"] = detect_result
        if arg.csrf:
            if arg.repeat is None:
                repeat_count = int(input("Enter the number of times to repeat the request: "))
            else:
                repeat_count = arg.repeat
            send_repeated_requests(arg.csrf, repeat_count, url)
            scan_report["results"]["csrf"] = {
                "request_file": arg.csrf,
                "repeats": repeat_count
            }
    except KeyboardInterrupt:
                print("⟪                                               ⟫")
                print("⟪ Stopping...                                   ⟫")
                print("⟪                                               ⟫")
                print("⟪±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±⟫")
                exit(1)
    finally:
        if driver is not None:
            driver.quit()

if arg.report:
    write_report(arg.report, scan_report)
    print(f"Report saved to: {arg.report}")

print("⟪                                               ⟫")
print("⟪±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±⟫")
