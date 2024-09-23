import os
import platform
import socket
import sys
from colorama import *
import json
import os
from datetime import datetime

def logo(url,response, count=0, pwd=0):
    
    os.system("cls" if os.name == "nt" else "clear")
    python_version = platform.python_version()
    code = response.status_code
    print(f"""
                        ░░░▒▒▒▒▒▒▒▒▒        
                     ░▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒       
                   ░▒▓▓▓█▓▓▒▒▓▒▓▒▓▓██▓▒     
                 ░▒▒▓▓▓▓▓▒▒▒▒░░▒▓▓▓▓▓▓██░   
                ░▒▓▓▒▓▒▒▒▒▒▒▒▒░▒▓▓▓▓▓▓▓█▓▒  
               ░▒▒▓▒░▓▓▒▒▒▒▒▒░▒▒▓▓▓▓▓▓▓▓██▓ 
               ░▒▓▒▒▒▒░▒▒▒▒▒▒░▒▓▓▓▓▓▓▓▓▓▓██░
               ░▒░▒▒▓▒▒▒▒▓▒░░▒███▓▓▓▓▓▓▓▓▓█▓
              ░▒░▒▒▓█░░░░░░░▒▓▓▓▓▓▓▓▓▓███▓▓▒
              ▒░░▒▒▓█▒░░░░░░▓▓▓▓▓██████▓▓▓▓░
              ░░░▒▓▓███▓▒░░▒▓███▓▓▓▓███▓▓▓▓░
             ░░░░▒▓▓███████████████▓▒░  ▓█▒ 
              ░░░▒▒▓███████████████▓░   ▓░  
             ░▒░░░░▒▒▓██████████▓▓▓▓░       
            ░▒▒▒▒▒░░▒▒▒▓▓████▓▓▒▒▓▓▒░       
          ░▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓░       
         ▒▓▒▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒        
        ░▓▓▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒░        
        ▒▒░▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒     
⟪===============================================⟫
    ░▒█▀▀▄░░▀░░▒█▀▀▄░░▀░░░░▒█▀▀▄░░▀░░█▀▀▄░█▀▄
    ░▒█▀▀▄░░█▀░▒█▀▀▄░░█▀░░░▒█▀▀▄░░█▀░█▄▄▀░█░█
    ░▒█▄▄█░▀▀▀░▒█▄▄█░▀▀▀░░░▒█▄▄█░▀▀▀░▀░▀▀░▀▀░
        
             - By Jeffrey Montanari
             - @alfredredbird1
             
⟪===============================================⟫
⟪                                               ⟫ 
⟪ OS:{platform.system()}                   Machine: {platform.machine()}   ⟫
⟪                                               ⟫                                            
⟪ Hostname: {socket.gethostname()}                  ⟫
⟪                                               ⟫ 
⟪ IP: {socket.gethostbyname(socket.gethostname())}                            ⟫ 
⟪                                               ⟫ 
⟪ Python Version: {Fore.YELLOW + python_version + Fore.RESET}                        ⟫ 
⟪                                               ⟫ 
⟪===============================================⟫ 
⟪                                               ⟫ 
⟪ Target: {url}  ⟫
⟪                                               ⟫ """)
    
    
    if code >= 400:
      print(f"⟪ Response: {Fore.RED + str(code) + Fore.RESET}                                 ⟫  ")
    if code <= 380:
      print(f"⟪ Response: {Fore.GREEN + str(code) + Fore.RESET}                                 ⟫  ")
      
    print("""⟪                                               ⟫  """)
    if count >= 1:
      print(f"""⟪ Input Elements: {count+pwd}                             ⟫""")
      print("⟪                                               ⟫")
      print(f"""⟪ Email Elements: {count}                             ⟫""")
      print("⟪                                               ⟫")
    if pwd >= 1:
      print(f"""⟪ Password Elements: {pwd}                          ⟫  
⟪                                               ⟫ 
⟪===============================================⟫ 
⟪                                               ⟫ """)






def save_to_json(url, count):
    filename = "data/gueses.json"
    data = {
        "url": url,
        "count": count,
        "date": datetime.now().isoformat()
    }

    # Check if the file exists
    if os.path.exists(filename):
        # Load existing data
        with open(filename, "r") as file:
            existing_data = json.load(file)
        # Append new data
        existing_data.append(data)
    else:
        # Create a new list with the first data entry
        existing_data = [data]

    # Write the updated data to the JSON file
    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)


def display_formatted_text(text, max_line_length=54):
    """
    Display text neatly with ⟪ and ⟫ around each line.
    Lines will wrap to a new line if they exceed the max_line_length,
    and shorter lines will be padded with spaces to match the length.
    Parameters:
    - text: The text to format and display.
    - max_line_length: The maximum number of characters per line.
    """
    # Make sure the text is not None
    if text is None:
        text = ""

    # Split the text into words to manage line wrapping
    words = text.split()
    current_line = ""
    formatted_output = []

    for word in words:
        # Check if adding the next word exceeds the line length
        if len(current_line) + len(word) + 1 <= max_line_length:
            # Add word to the current line
            current_line += (word + " ")
        else:
            # Add the current line to formatted_output, trim trailing spaces, and pad
            formatted_output.append(f"⟪ {current_line.strip():<{max_line_length}} ⟫")
            # Start a new line with the current word
            current_line = word + " "

    # Add the last line if any remaining, and pad
    if current_line:
        formatted_output.append(f"⟪ {current_line.strip():<{max_line_length}} ⟫")

    # Print the formatted lines
    for line in formatted_output:
        print(line)


# Example usage for request analysis
def print_request_details(method, url, headers, body_data):
    """
    Display request details using formatted text function.
    """
    display_formatted_text(f"Request Method: {method}")
    print("⟪                                                        ⟫")
    display_formatted_text(f"Request URL: {url}")

    if headers:
        display_formatted_text("Headers:")
        print("⟪                                                        ⟫")
        for header, value in headers.items():
            display_formatted_text(f"{header}: {value}")
            print("⟪                                                        ⟫")
    if body_data:
        display_formatted_text("Body Data:")
        print("⟪                                                        ⟫")
        display_formatted_text(json.dumps(body_data, indent=2))
    else:
        display_formatted_text("No Body Data")
        print("⟪                                                        ⟫")

