from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/servicenow-data', methods=['GET'])
def get_servicenow_data():
    auth_url = "https://bakerhughes.service-now.com/oauth_token.do"
    auth_data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)
    access_token = auth_response.json().get("access_token")

    api_url = "https://bakerhughes.service-now.com/api/now/v1/table/incident?assignment_group=L1_BH_RPACOE_ProdSupport"
    api_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    api_response = requests.get(api_url, headers=api_headers)
    data = api_response.json().get("result", [])

    # Return only selected fields
    filtered_data = [
        {
            "number": item.get("number"),
            "short_description": item.get("short_description"),
            "assigned_to": item.get("assigned_to"),
            "opened_at": item.get("opened_at"),
            "closed_at": item.get("closed_at"),
            "incident_state": item.get("incident_state")
        }
        for item in data
    ]

    return jsonify(filtered_data)
