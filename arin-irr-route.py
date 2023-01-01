#!/bin/python3
import argparse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Set the API key and abuse contact email from the environment variables
api_key = os.getenv("ARIN_API_KEY")
abuse_contact_email = os.getenv("ABUSE_CONTACT_EMAIL")

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("route", help="The IPv4 route to be added to the IRR record")
parser.add_argument("originas", help="The source ASN for the route")
args = parser.parse_args()

# Set the route and source ASN from the command-line arguments
route = args.route
originas = args.originas

# Set the IRR record parameters
payload = f"""route: {route}
origin: AS{originas}
descr: ANY ABUSE SHOULD BE REPORTED TO {abuse_contact_email}
mnt-by: MNT-CANAD-111
admin-c: NOC33562-ARIN
tech-c: NOC33562-ARIN
source: ARIN
"""

# Set the HTTP headers
headers = {
    "Content-Type": "application/rpsl",
    "Accept": "application/rpsl"
}

# Make the API request to create the IRR record
response = requests.post(f"https://reg.arin.net/rest/irr/route/{route}/AS{originas}?apikey={api_key}", headers=headers, data=payload)

# Check the API response
if response.status_code == 200:
    print("IRR record created successfully")
else:
    print("Error creating IRR record: {}".format(response.text))
