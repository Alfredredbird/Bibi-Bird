<div align=center>
    
![bibi-bird-480-text](https://github.com/user-attachments/assets/a0836bfa-6012-4502-b891-2416222bb0f2)
</div>

#  Overview
Bibi Bird is a tool writen in python that tests websites for SQL Injections, XSS and other vulnerabilities. My tool is still in beta but works 90% of the time.


# Installation

    git clone https://github.com/alfredredbird/Bibi-Bird
    cd Bibi-Bird && sudo pip3 install -r requirements.txt
    python3 main.py

# Manual Install

    download the latest release from: https://github.com/alfredredbird/Bibi-Bird/releases.
    then extract the zip or tar.gz

    cd Bibi-Bird && sudo pip3 install -r requirements.txt
    python3 Bibi-Bird

# CLI Modes

- SQL injection mode: `python3 main.py -u https://target.tld/login -i`
- SQL injection with custom wordlist: `python3 main.py -u https://target.tld/login -i -w dict/sql-common.txt`
- SQL error detection mode: `python3 main.py -u https://target.tld/page --sql-detect`
- XSS URL mode: `python3 main.py -u "https://target.tld/search?" -x 1`
- XSS form mode: `python3 main.py -u https://target.tld/login -x 2`
- CSRF request replay mode: `python3 main.py -u https://target.tld -c tests/request.txt -r 25`
- Save report output: `python3 main.py -u https://target.tld -i --report data/report.json`

# Tested OS

<table>
    <tr>
        <th>Operative system</th>
        <th> Version </th>
    </tr>
    <tr>
        <td>MacOS</td>
        <td> Monterey 12.6.7 </td>
    </tr>
    <tr>
        <td>Windows</td>
        <td>11/10</td>
    </tr>
    <tr>
        <td>Kali linux</td>
        <td> Rolling / Sana</td>
    </tr>
    <tr>
        <td>Parrot OS</td>
        <td>3.1 </td>
    </tr>
    <tr>
        <td>Ubuntu</td>
        <td>22.04/20.04 </td>
    </tr>
    <tr>
        <td>Debian</td>
        <td>10.00 </td>
    </tr>
   <tr>
        <td>Alpine</td>
        <td>3.10 </td>
    </tr>
  <tr>
        <td>Fedora</td>
        <td>v33</td>
    </tr>
  <tr>
        <td>Arch Linux</td>
        <td>2021.07.01</td>
    </tr>
    <tr>
        <td>Manjaro</td>
        <td>21</td>
    </tr>
   <tr>
        <td>Void</td>
        <td>Rolling Release</td>
    </tr>
</table>

# Requirements

There Is A Lot Lol

- colorama 
- requests 
- selenium
- alive_progress
- bs4

# Supported Languages
>(we need translators)
- [x] English
- [ ] Italian
- [ ] Hebrew 
- [ ] Spanish
- [ ] French 
- [ ] Arabic
- [ ] German
- [ ] Hindi
- [ ] Russian
- [ ] Portuguese

# Upcoming Features
 (They Are Great First Issues :D)

 - [x] SQL Injections
 - [x] SQL Detections
 - [ ] DNS Scanning
 - [ ] URL Brute Forcing
 - [x] Reports
 - [X] XSS Injecting
 - [ ] Site OSINT
 - [x] Custom Wordlists
 - [ ] Payload Generation
 - [X] Payload Selection
 - [X] CSRF Attacks (beta)

# Need Help?
Check out [Bibi-Bird/issues](https://github.com/alfredredbird/Bibi-Bird/issues) or the WiKi for help.
Still Need Help? Contact Below :D

# Info:

<table>
    <tr>
        <th>Wiki</th>
        <th>https://github.com/alfredredbird/Bibi-Bird/wiki</th>
    </tr>
   <tr>
        <th>Releases</th>
        <th>https://github.com/alfredredbird/Bibi-Bird/releases</th>
    </tr>
    <tr>
        <th>Contributors</th>
        <th>https://github.com/alfredredbird/Bibi-Bird/graphs/contributors</th>
    </tr>
</table>

# Contact

- Twitter: [alfredredbird1](https://twitter.com/alfredredbird1)
- LinkedIn: [jeffrey montanari](https://www.linkedin.com/in/jeffrey-montanari-7178a1290)

# Other Tools

Other tools in the fleet:
- Tookie-OSINT: [Tookie-OSINT](http://github.com/alfredredbird/tookie-osint)
  
# Partnership
Want to partner with the Bibi-Bird project? Feel free to reach out!

  partners:

  ~ Mrofcodyx - [Git-eXpossed](https://github.com/mrofcodyx/Git-eXposed)
