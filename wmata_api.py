'''
Email: lnovelo1@jh.edu
Course: Intro to Python
Module 10: Building an Automated CI/CD Pipeline
'''

import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "cb68321087a648f2bb5043d0e4f1c29f"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

# To access, go here: http://127.0.0.1:5000/incidents/elevators and http://127.0.0.1:5000/incidents/escalators

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []

    # use 'requests' to do a GET request to the WMATA Incidents API
    unit_type_lower = unit_type.lower()
    if unit_type_lower == "elevators":
        url = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
        expected_type = "ELEVATOR"
    elif unit_type_lower == "escalators":
        url = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
        expected_type = "ESCALATOR"
    else:
        return json.dumps({"error": "Invalid unit type provided. Use 'elevators' or 'escalators'."}), 400
    
    # retrieve the JSON from the response
    response = requests.get(url, headers=headers)
    data = response.json()
    incidents_data = data.get("ElevatorIncidents", [])
    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    for incident in incidents_data:
            # Optionally, check if the UnitType matches what we expect
        if incident.get("UnitType", "").upper() == expected_type:
        # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
        #   -StationCode, StationName, UnitType, UnitName
            incident_dict = {
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitName": incident.get("UnitName"),
                "UnitType": incident.get("UnitType")
            }
            # add each incident dictionary object to the 'incidents' list
            incidents.append(incident_dict)
            
    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)