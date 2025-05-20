from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv
import time

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
    try:
        # Step 1: Get access token
        auth_url = "https://bakerhughes.service-now.com/oauth_token.do"
        auth_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN
        }
        auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        start = time.time()
        auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers, timeout=30)
        print("Token request took", time.time() - start, "seconds")

        if auth_response.status_code != 200:
            print("Failed to get access token:", auth_response.text)
            return jsonify({"error": "Failed to get access token", "details": auth_response.text}), 500

        access_token = auth_response.json().get("access_token")
        print("Access token received:", access_token)

        # Step 2: Call ServiceNow API
        api_url = "https://bakerhughes.service-now.com/api/now/v1/table/incident?assignment_group=L1_BH_RPACOE_ProdSupport"
        api_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        start = time.time()
        api_response = requests.get(api_url, headers=api_headers, timeout=90)
        print("ServiceNow API call took", time.time() - start, "seconds")

        if api_response.status_code != 200:
            print("Failed to fetch incident data:", api_response.text)
            return jsonify({"error": "Failed to fetch incident data", "details": api_response.text}), 500

        return jsonify(api_response.json())

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return jsonify({"error": "Request failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
