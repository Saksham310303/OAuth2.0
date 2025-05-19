from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

# Get credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
print("REFRESH_TOKEN:", REFRESH_TOKEN)

@app.route('/servicenow-data', methods=['GET'])
def get_servicenow_data():
    # Step 1: Get access token
    auth_url = "https://bakerhughes.service-now.com/oauth_token.do"
    auth_data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

    if auth_response.status_code != 200:
        return jsonify({"error": "Failed to get access token", "details": auth_response.text}), 500

    access_token = auth_response.json().get("access_token")

    # Step 2: Call ServiceNow API
    api_url = "https://bakerhughes.service-now.com/api/now/v1/table/incident?assignment_group=L1_BH_RPACOE_ProdSupport"
    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    api_response = requests.get(api_url, headers=api_headers)

    if api_response.status_code != 200:
        return jsonify({"error": "Failed to fetch incident data", "details": api_response.text}), 500

    return jsonify(api_response.json())

if __name__ == '__main__':
    app.run(debug=True)


#i have two python files which I need to deploy on a free hosting platform so I can use the service-now api with oauth2 authentication after it has been published, did you understand my problem?