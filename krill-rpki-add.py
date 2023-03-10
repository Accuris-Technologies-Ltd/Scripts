#!/bin/python3
import argparse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

krill_url = os.getenv("KRILL_URL")
krill_ca = os.getenv("KRILL_CA")
api_key = os.getenv("KRILL_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument("route", help="The IPv4 route to be added to the ROA record")
parser.add_argument("originas", help="The source ASN for the route")
parser.add_argument("maxlen", help="The maximum length of the route")
args = parser.parse_args()

# Set the route and source ASN from the command-line arguments
route = args.route
originas = args.originas
maxlen = args.maxlen

# Set the HTTP headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + str(api_key)
}

data = {
    "added": [
    {
        "asn": int(originas),
        "prefix": route,
        "max_length": int(maxlen)
    }
    ],
    "removed": []
}

# Make the API request to create the IRR record
response = requests.post(f"https://{krill_url}/api/v1/cas/{krill_ca}/routes", headers=headers, json=data)

# Check the API response
if response.status_code == 200:
    print("ROA created successfully")
else:
    print("Error creating ROA: {}".format(response.text))
