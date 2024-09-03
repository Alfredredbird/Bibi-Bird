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
⟪ Hostname: {socket.gethostname()}        IP: {socket.gethostbyname(socket.gethostname())} ⟫
⟪                                               ⟫ 
⟪ Python Version: {Fore.YELLOW + python_version + Fore.RESET}                        ⟫ 
⟪                                               ⟫ 
⟪===============================================⟫ 
⟪                                               ⟫ 
⟪ Target: {url}    ⟫
⟪                                               ⟫ """)
    
    
    if code >= 400:
      print(f"⟪ Response: {Fore.RED + str(code) + Fore.RESET}                                 ⟫  ")
    if code <= 380:
      print(f"⟪ Response: {Fore.GREEN + str(code) + Fore.RESET}                                 ⟫  ")
      
    print("""⟪                                               ⟫  """)
    if count >= 1:
      print(f"""⟪ Input Elements: {count}                             ⟫""")
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

# Example usage:

