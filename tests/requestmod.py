import re
import json
import requests
import random
import string
################################################################
#
# THIS IS FOR TESTING
#
################################################################
def load_values(file_path):
    """Load search keys from a text file, one key per line."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def analyze_request_file(request_file, values_file):
    # Load keys to search for
    search_keys = load_values(values_file)

    with open(request_file, 'r') as file:
        # Read file content
        request_data = file.read()

    # Split request into headers and body (if any)
    try:
        headers_part, body_part = request_data.split('\n\n', 1)
    except ValueError:
        headers_part, body_part = request_data, None

    # Split the header lines
    header_lines = headers_part.splitlines()

    # Parse request line (e.g., "POST /api/Users/ HTTP/1.1")
    request_line = header_lines[0]
    method, url, http_version = request_line.split()

    # Ensure the URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'http://192.168.12.146:3000' + url  # Update the host as needed

    # Parse headers
    headers = {}
    header_regex = re.compile(r'^(.*?):\s(.*)$')
    for line in header_lines[1:]:
        match = header_regex.match(line)
        if match:
            headers[match.group(1)] = match.group(2)

    # Try to parse body as JSON if content type indicates JSON
    body_data = None
    if body_part and headers.get('Content-Type') == 'application/json':
        try:
            body_data = json.loads(body_part)
        except json.JSONDecodeError:
            body_data = body_part  # Fallback to raw body if not JSON

    # Print out request analysis
    print("Request Method:", method)
    print("Request URL:", url)
    print("HTTP Version:", http_version)
    print("Headers:", json.dumps(headers, indent=2))
    print("Body Data:", json.dumps(body_data, indent=2) if body_data else "No Body")

    # Search for keys in the body data
    found_keys = {}
    if body_data and isinstance(body_data, dict):
        for key in search_keys:
            if key in body_data:
                found_keys[key] = body_data[key]

    # Print out found keys and their values
    if found_keys:
        print("\nFound keys and values in the body:")
        for key, value in found_keys.items():
            print(f"Found key: {key}, Value: {value}")

        # Edit keys if the user chooses to do so
        while True:
            edit_key = input("\nEnter the key you want to edit (or 'exit' to stop editing): ")
            if edit_key in found_keys:
                new_value = input(f"Enter new value for '{edit_key}' (current value: {found_keys[edit_key]}): ")
                body_data[edit_key] = new_value
                print(f"Updated '{edit_key}' to: {new_value}")
            elif edit_key.lower() == 'exit':
                print("Stopping edits.")
                break
            else:
                print("Key not found. No changes made.")

    # Print modified body
    print("\nModified Body Data:", json.dumps(body_data, indent=2) if body_data else "No Body")

    # Return request details for sending
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "body": body_data,
        "found_keys": found_keys  # Include found keys for brute forcing
    }

def random_string(length=8, char_set=string.ascii_letters + string.digits):
    """Generate a random string of fixed length from the specified character set."""
    return ''.join(random.choice(char_set) for i in range(length))

def send_repeated_requests(request_file, values_file, repeat_count):
    """Send a modified request multiple times, with optional brute-forcing."""
    request_details = analyze_request_file(request_file, values_file)
    
    if not request_details:
        print("No valid request details found. Exiting.")
        return

    method = request_details["method"]
    url = request_details["url"]
    headers = request_details["headers"]
    body_data = request_details["body"]
    found_keys = request_details["found_keys"]

    # Prompt for a key to brute force
    if found_keys:
        print("\nKeys available for brute forcing:")
        for idx, key in enumerate(found_keys.keys(), 1):
            print(f"{idx}. {key}")

        choice = input("\nEnter the number of the key you want to brute force: ")
        try:
            brute_force_key = list(found_keys.keys())[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Exiting.")
            return
    else:
        print("No keys found for brute forcing. Exiting.")
        return

    # Ask the user for the type of brute force
    print("\nChoose the type of brute force:")
    print("1. Email format (e.g., user@example.com)")
    print("2. Letters only")
    print("3. Numbers only")
    print("4. Mix of letters and numbers")
    brute_force_type = input("Enter the number of the brute force type: ")

    email_endings = []  # Initialize email endings list

    for i in range(repeat_count):
        print(f"\nSending request {i + 1}/{repeat_count}...")

        # Randomize the value for the brute-force key based on the selected type
        if brute_force_key and body_data and isinstance(body_data, dict):
            if brute_force_type == '1':
                # Ask for email endings
                if not email_endings:
                    email_endings = input("Enter the email endings separated by commas (e.g., @parrot.com,@gmail.com): ").split(',')
                body_data[brute_force_key] = random_string(8) + random.choice(email_endings).strip()
            elif brute_force_type == '2':
                body_data[brute_force_key] = random_string(8, string.ascii_letters)  # Letters only
            elif brute_force_type == '3':
                body_data[brute_force_key] = random_string(10, string.digits)  # Numbers only
            elif brute_force_type == '4':
                body_data[brute_force_key] = random_string(8, string.ascii_letters + string.digits)  # Mix
            else:
                print("Invalid brute force type. Exiting.")
                return
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=body_data)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=body_data)
            else:
                print("Unsupported HTTP method. Only GET and POST are supported.")
                continue

            # Print response from the server
            print(f"Response {i + 1} Status Code:", response.status_code)
            print(f"Response {i + 1} Body:", response.text)
        except requests.RequestException as e:
            print(f"Request {i + 1} failed: {e}")

# Example usage
request_file = 'request.txt'  # Path to your file containing the HTTP request data
values_file = 'values.txt'  # Path to the file containing keys to search for
repeat_count = int(input("Enter the number of times to repeat the request: "))  # User-defined repeat count

send_repeated_requests(request_file, values_file, repeat_count)
