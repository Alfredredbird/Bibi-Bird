import os
import platform
import socket
import sys
from colorama import *


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
⟪ Python Version: {python_version}                        ⟫ 
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
