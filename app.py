from flask import Flask, jsonify, request
import requests
import json
import time
from datetime import datetime
from pyBSDate import convert_AD_to_BS

app = Flask(__name__)

def convert_to_bs(date_str):
    # Convert AD date to BS using pyBSDate
    ad_date = datetime.strptime(date_str, "%Y-%m-%d")
    try:
        bs_date_tuple = convert_AD_to_BS(ad_date.year, ad_date.month, ad_date.day)
        bs_date = datetime(*bs_date_tuple)  # Convert the tuple to datetime
        return bs_date
    except ValueError:
        return None

# Shared URL and headers
url = "https://www.sharesansar.com/existing-issues"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.sharesansar.com/existing-issues",
    "X-Requested-With": "XMLHttpRequest",
}

def fetch_data(type_value, limit=20):  # Default limit is set to 20
    current_timestamp = int(time.time() * 1000)
    payload = {
        "draw": 1,
        "columns[0][data]": "DT_Row_Index",
        "columns[0][name]": "",
        "columns[0][searchable]": "false",
        "columns[0][orderable]": "false",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "start": 0,
        "length": limit,  # Use the limit parameter
        "search[value]": "",
        "search[regex]": "false",
        "type": type_value,
        "_": current_timestamp,
    }
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code == 200:
        data = response.json()["data"]
        formatted_data = []
        for entry in data:
            opening_date_ad = entry["opening_date"] if entry["opening_date"] else None
            closing_date_ad = entry["closing_date"] if entry["closing_date"] else None
            extended_closing_date_ad = entry["final_date"] if entry["final_date"] else None

            opening_date_bs = convert_to_bs(opening_date_ad) if opening_date_ad else None
            closing_date_bs = convert_to_bs(closing_date_ad) if closing_date_ad else None
            extended_closing_date_bs = convert_to_bs(extended_closing_date_ad) if extended_closing_date_ad else None

            # Updated logic for setting the status
            if entry["status"] == 0:
                status = "Open"
            elif entry["status"] == 1:
                status = "Closed"
            elif entry["status"] == -2:
                status = "In Progress"
            else:
                status = "Unknown"

            formatted_entry = {
                "companyName": entry["company"]["companyname"].split('>')[1].split('<')[0],
                "companySymbol": entry["company"]["symbol"].split('>')[1].split('<')[0],
                "units": entry["total_units"],
                "price": entry["issue_price"],
                "openingDateAd": opening_date_ad if opening_date_ad else "In Progress",
                "closingDateAd": closing_date_ad if closing_date_ad else "In Progress",
                "extendedClosingDateAd": extended_closing_date_ad if extended_closing_date_ad else "In Progress",
                "openingDateBs": opening_date_bs.strftime("%Y-%m-%d") if opening_date_bs else "In Progress",
                "closingDateBs": closing_date_bs.strftime("%Y-%m-%d") if closing_date_bs else "In Progress",
                "extendedClosingDateBs": extended_closing_date_bs.strftime("%Y-%m-%d") if extended_closing_date_bs else "In Progress",
                "listingDate": entry["listing_date"] if entry["listing_date"] else "",
                "issueManager": entry["issue_manager"],
                "status": status,
            }
            formatted_data.append(formatted_entry)
        return formatted_data
    else:
        raise Exception(f"Error: {response.status_code}")

# Define your Flask routes here as in your original code...

if __name__ == '__main__':
    app.run(debug=True)
