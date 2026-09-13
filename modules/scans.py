import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from modules.mods import *
import requests
import string 
import random
import json
from pathlib import Path
from urllib.parse import urljoin
from colorama import *

box_width = 49
BASE_DIR = Path(__file__).resolve().parent.parent

SQL_ERROR_PATTERNS = [
    "sql syntax",
    "mysql",
    "unclosed quotation mark",
    "odbc sql server",
    "sqlstate",
    "postgresql",
    "sqlite error",
    "oracle error",
    "warning: pg_",
    "syntax error at or near"
]

# Function to create a fixed-width line bc it line wraps sometimes
def create_box_line(content, width, align="left"):
    if align == "left":
        return f"⟪ {content.ljust(width - 4)} ⟫"
    elif align == "right":
        return f"⟪ {content.rjust(width - 4)} ⟫"
    elif align == "center":
        return f"⟪ {content.center(width - 4)} ⟫"

def generate_random_string(length=8):
    # Define the characters to choose from: letters (uppercase and lowercase) and digits
    characters = string.ascii_letters + string.digits
    # Generate a random string by selecting random characters from the defined set
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def _read_lines(path):
    try:
        with open(path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Missing file: {path}")
        return []


def _dedupe_elements(elements):
    unique = []
    seen = set()
    for element in elements:
        key = element.id
        if key not in seen:
            unique.append(element)
            seen.add(key)
    return unique


def _find_elements(driver, selectors):
    found = []
    for selector in selectors:
        try:
            if selector.startswith('//'):
                found.extend(driver.find_elements(By.XPATH, selector))
            else:
                found.extend(driver.find_elements(By.NAME, selector))
                found.extend(driver.find_elements(By.ID, selector))
                found.extend(driver.find_elements(By.CSS_SELECTOR, f"[placeholder='{selector}']"))
        except Exception as e:
            print(f"Error finding selector {selector}: {e}")
    return _dedupe_elements(found)

def inject(url, driver, response, wordlist, payload, delay):
    result = {
        "queued": 0,
        "tested": 0,
        "working_payload": "",
        "redirected_to": "",
        "sql_error_detected": False
    }

    driver.get(url)

    password_selectors = _read_lines(BASE_DIR / "data" / "PassSelectors.txt")
    email_selectors = _read_lines(BASE_DIR / "data" / "EmailSelectors.txt")

    password_elements = _find_elements(driver, password_selectors)
    email_elements = _find_elements(driver, email_selectors)

    # Count the elements
    pwd = len(password_elements)
    count = len(email_elements)


    # Call the logo function
    logo(url, response, count, pwd)
    if not email_elements or not password_elements:
        print("⟪ Could not find enough form elements to run SQL injection mode. ⟫")
        return result

    # reading and deciding the payloads
    if payload == 1 or payload == 0:
        if payload == 0:
            print(f"⟪ {Fore.RED + 'Using Default Wordlist' + Fore.RESET}                        ⟫")
            print("⟪                                               ⟫")
        lines = _read_lines(BASE_DIR / 'dict' / 'sql-common.txt')

    if payload == 2:
        lines = _read_lines(BASE_DIR / 'dict' / 'sql-generic.txt')

    if payload == 3:
        lines = _read_lines(BASE_DIR / 'dict' / 'sql-time.txt')

    if wordlist:
        custom_lines = _read_lines(wordlist)
        if custom_lines:
            lines = custom_lines

    if not lines:
        print("⟪ No payloads available. Check your wordlist files. ⟫")
        return result

    email_credentials = [line.strip() for line in lines if line.strip()]

    # email_credentials = ["admin' OR '1'='1'--", "user@example.com"]
    password_credentials = ["parrot"]

    lenemail = len(email_credentials)
    result["queued"] = lenemail
    if lenemail <= 2:
        print(f"⟪ Injections Loaded: {Fore.RED + str(lenemail) + Fore.RESET}                         ⟫")
    if lenemail >= 20 and lenemail <= 39:
        print(f"⟪ Injections Loaded: {Fore.YELLOW + str(lenemail) + Fore.RESET}                         ⟫")
    if lenemail >= 40:
        print(f"⟪ Injections Loaded: {Fore.GREEN + str(lenemail) + Fore.RESET}                         ⟫")
    
    print("⟪                                               ⟫")
    print("⟪ Injection Queue:                              ⟫")
    print("⟪                                               ⟫")
    last_payload = ""

    for email in email_credentials:
        for password in password_credentials:
            try:
                for element in email_elements:
                    element.clear()
                    element.send_keys(email)
                print(create_box_line(f"  {result['tested']}.  {email}", box_width, "left"))
                result["tested"] += 1
                last_payload = email
                

                # Send keys to the password elements
                for element in password_elements:
                    element.clear()
                    element.send_keys(password)
                    
                
                # Press Enter after filling out the forms
                password_elements[0].send_keys(Keys.RETURN)
                time.sleep(max(delay, 0))

                source = driver.page_source.lower()
                if any(pattern in source for pattern in SQL_ERROR_PATTERNS):
                    result["sql_error_detected"] = True

            except Exception as e:
                pass
            except KeyboardInterrupt:
                print("⟪                                               ⟫")
                print("⟪ Stopping...                                   ⟫")
                print("⟪                                               ⟫")
                print(create_box_line(f"Last Injection: {Fore.RED + last_payload + Fore.RESET}", 59, "left"))
                print("⟪                                               ⟫")
                print("⟪±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±±⟫")
                exit(1)
                
    
    # Wait for the page to potentially redirect
    # Check if the URL has changed (indicating a redirect)
    current_url = driver.current_url
    
    if current_url != url:
        print("⟪                                               ⟫")
        print("⟪===============================================⟫ ")
        print("⟪                                               ⟫")
        print(create_box_line(f"Working Injection: {Fore.YELLOW + last_payload + Fore.RESET}", 59, "left"))
        print(f"⟪                                               ⟫")
        print(f"⟪ Redirection:                                  ⟫")
        print("⟪                                               ⟫")
        print(f"⟪ {current_url}           ⟫")
        result["working_payload"] = last_payload
        result["redirected_to"] = current_url
        if current_url != "": 
            print("⟪                                               ⟫")
            print(create_box_line(f"Injection: {Fore.GREEN + 'Successful' + Fore.RESET}", 59, "left"))
            save_to_json(url, result["tested"])
            print("⟪                                               ⟫")
        else:
            print(create_box_line(f"Injection: {Fore.RED + 'Failure :(' + Fore.RESET}", 49, "left"))           
    return result
    

def brute(url,driver,response):
    print("⟪===============================================⟫")
    print("⟪                                               ⟫")
    print("⟪ Bruting:                                      ⟫")
    print("⟪                                               ⟫")
    i = 0
    while i <= 32:
        rq = requests.get(url + generate_random_string(4))
        print(f"⟪ {i}. {url + generate_random_string(4)}: {rq.status_code}     ⟫")
        i += 1
    
def subdomain(url, driver, wordlist):
    
    driver.get(url)
    homecode = driver.page_source.strip()  # Strip whitespace from homepage code
    
    print("Home Page Source Captured.")
    
    lines = _read_lines(wordlist)
    found = []
        
    for line in lines:
        line = line.strip()  # Strip whitespace from each line
        if not line:  # Skip empty lines
            continue
            
        newurl = urljoin(url.rstrip('/') + '/', line)
        
        try:
            driver.get(newurl)
            domaincode = driver.page_source.strip()  # Strip whitespace from domain code
            print("⟪                                               ⟫")
            if homecode == domaincode:
                pass
            else:
                print(create_box_line(f"{newurl}", 49, "left"))
                found.append(newurl)
                
        except Exception as e:
            print(f"Error accessing {newurl}: {e}")
    return found

# Function to handle alerts and continue
def handle_alert(driver):
    try:
        # Switch to the alert and accept it
        alert = driver.switch_to.alert
        print("⟪                                               ⟫")
        print("⟪===============================================⟫")
        print("⟪                                               ⟫")
        print(f"⟪ Alert detected: {alert.text}                             ⟫")
        print("⟪                                               ⟫")
        alert.accept()
    except NoAlertPresentException:
        # No alert to handle
        pass

def xssScan(driver, url, mode=1):
    result = {
        "mode": mode,
        "tested": 0,
        "reflected": 0,
        "alerts": 0
    }

    xss_payloads = _read_lines(BASE_DIR / 'dict' / 'xss-common.txt')
    if not xss_payloads:
        print("⟪ No XSS payloads loaded. ⟫")
        return result

    if mode == 1:
        print("⟪===============================================⟫")
        print("⟪                                               ⟫")
        print("⟪ Scanning For XSS In URL:                      ⟫")
        print("⟪                                               ⟫")

        param_name = "q"
        for payload in xss_payloads:
            vulnerable_url = f"{url}{param_name}={payload}"
            print(create_box_line(f"{param_name}={payload}", 49, "left"))
            try:
                driver.get(vulnerable_url)
                time.sleep(2)
                result["tested"] += 1

                handle_alert(driver)

                page_source = driver.page_source
                if payload in page_source:
                    result["reflected"] += 1
                    print(create_box_line(f"Reflected: {payload}", 49, "left"))
            except UnexpectedAlertPresentException:
                result["alerts"] += 1
                handle_alert(driver)

        return result

    if mode == 2:
        driver.get(url)
        time.sleep(2)

        inputs = driver.find_elements(By.TAG_NAME, 'input')
        input_count = len(inputs)
        working_count = []

        print("⟪                                               ⟫")
        print("⟪===============================================⟫")
        print("⟪                                               ⟫")
        print(f"⟪ Input Fields: {input_count}                               ⟫")
        print("⟪                                               ⟫")
        if len(xss_payloads) <= 8:
            print(f"⟪ Payloads Loaded: {Fore.RED + str(len(xss_payloads)) + Fore.RESET}                            ⟫")
        if len(xss_payloads) >= 8 and len(xss_payloads) <= 16:
            print(f"⟪ Payloads Loaded: {Fore.YELLOW + str(len(xss_payloads)) + Fore.RESET}                            ⟫")
        if len(xss_payloads) >= 17:
            print(f"⟪ Payloads Loaded: {Fore.GREEN + str(len(xss_payloads)) + Fore.RESET}                          ⟫")

        print("⟪                                               ⟫")
        print("⟪===============================================⟫")
        print("⟪                                               ⟫")
        print("⟪ Payload Queue:                                ⟫")
        print("⟪                                               ⟫")

        for payload in xss_payloads:
            for input_field in inputs:
                try:
                    input_field.clear()
                    input_field.send_keys(payload)
                    input_field.send_keys(Keys.RETURN)
                    time.sleep(2)

                    page_source = driver.page_source
                    print(create_box_line(f" {payload}", 49, "left"))
                    result["tested"] += 1
                    if payload in page_source:
                        working_count.append(payload)
                        result["reflected"] += 1
                except Exception:
                    try:
                        alert = driver.switch_to.alert
                        print("⟪                                               ⟫")
                        print(create_box_line(f" {payload}", 49, "left"))
                        alert.accept()
                        result["alerts"] += 1
                    except Exception:
                        print("⟪                                               ⟫")
                        print("⟪===============================================⟫")
                        print("⟪                                               ⟫")
                        print(f"⟪ {Fore.RED + 'Error!' + Fore.RESET} Can't Interact With Element!           ⟫")
                        return result

        print(f"Working Payloads: {len(working_count)}")
        return result

    print("⟪ Unknown XSS mode selected. Use 1 or 2. ⟫")
    return result


def detect_sql_errors(url, headers):
    probes = ["'", '"', "')", "--", "' OR '1'='1"]
    findings = []

    for probe in probes:
        test_url = f"{url}?id={probe}"
        try:
            response = requests.get(test_url, headers=headers, timeout=15)
            body = response.text.lower()
            matched = [p for p in SQL_ERROR_PATTERNS if p in body]
            if matched:
                findings.append({
                    "probe": probe,
                    "status": response.status_code,
                    "matched_patterns": matched,
                    "url": test_url
                })
                print(create_box_line(f"SQL pattern hit with probe: {probe}", 49, "left"))
        except requests.RequestException as e:
            print(f"Request failed for probe {probe}: {e}")

    print(create_box_line(f"SQL detection findings: {len(findings)}", 49, "left"))
    return {
        "findings": findings,
        "count": len(findings)
    }
