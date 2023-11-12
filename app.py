from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route('/get_upcoming_ipo', methods=['GET'])
def get_upcoming_ipo():
    # Replace the headless browser code with direct HTTP request
    url = 'https://www.sharesansar.com/existing-issues#ipo'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract table data and convert it to a list of dictionaries
    data_list = []
    table = soup.find('table', {'id': 'myTableEip'})
    if table:
        for row in table.tbody.find_all('tr'):
            columns = row.find_all(['td', 'th'])
            data_list.append({
                "companyName": columns[2].text.strip(),
                "companySymbol": columns[1].text.strip(),
                "units": columns[3].text.strip(),
                "price": columns[4].text.strip(),
                "openingDate": columns[5].text.strip(),
                "closingDate": columns[6].text.strip(),
                "extendedClosingDate": columns[7].text.strip(),
                "listingDate": columns[8].text.strip(),
                "issueManager": columns[9].text.strip(),
                "status": columns[10].text.strip()
            })

    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(data_list, indent=2)

    # Return the JSON data as the API response
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
