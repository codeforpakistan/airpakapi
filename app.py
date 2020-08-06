import os
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup


# Constants
DETAILS_PAGE_URL = 'http://www.pmd.gov.pk/rnd/rndweb/rnd_new/R%20&%20D.php'

# Initilizing app
app = Flask(__name__)
CORS(app)

# Home Page
@app.route('/')
def home():
    return 'Hello from Airpak API.'

# Details Page
@app.route('/pollendetails/<string:city>', methods=['GET'])
def get_doctor_details(city: str):

    if city.lower() not in ['islamabad']:
        return jsonify({
            'success': False,
            'message': f'No Record Found for "{city}"'
        }), 404

    page = get(DETAILS_PAGE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    result = {city: []}
    obj = soup.select_one('#dvPractitioners > tr:nth-child(1) > td:nth-child(1)')
    
    try:
        for i in range(1, 100):
            
            check = soup.select_one(f'#rounded-corner > tbody > tr:nth-child({i}) > td:nth-child(1)')
            if check is None: break

            result[city].append({
                'type': soup.select_one(f'#rounded-corner > tbody > tr:nth-child({i}) > td:nth-child(1)').getText(),
                'h-8': soup.select_one(f'#rounded-corner > tbody > tr:nth-child({i}) > td:nth-child(2)').getText(),
                'category': soup.select_one(f'#rounded-corner > tbody > tr:nth-child({i}) > td:nth-child(3)').getText()
            })
    except Exception as e:
        print(f'Unable to get pollen details from site. Error: {str(e)}')

    return jsonify(result), 200
