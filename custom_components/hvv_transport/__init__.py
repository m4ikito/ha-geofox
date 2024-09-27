import logging
import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant

DOMAIN = "hvv_transport"
LOGGER = logging.getLogger(__name__)

def create_signature(body: str, password: str) -> str:
    """Erstellt eine HMAC-SHA1 Signatur für die API-Anfrage."""
    message = body.encode('utf-8')
    secret = password.encode('utf-8')
    signature = hmac.new(secret, message, hashlib.sha1).digest()
    return base64.b64encode(signature).decode()

def check_name(username: str, password: str, station_name: str) -> dict:
    """Fragt die API nach Haltestelleninformationen."""
    request_body = {
        "version": 59,
        "theName": {
            "name": station_name,
            "type": "UNKNOWN"
        },
        "maxList": 1,
        "coordinateType": "EPSG_4326"
    }

    body = json.dumps(request_body)
    signature = create_signature(body, password)

    headers = {
        "Content-Type": "application/json",
        "geofox-auth-type": "HmacSHA1",
        "geofox-auth-user": username,
        "geofox-auth-signature": signature,
    }

    response = requests.post("https://gti.geofox.de/gti/public/checkName", headers=headers, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        LOGGER.error(f"HTTP Fehler bei checkName: {response.status_code}")
        LOGGER.error(f"Fehlerdetails: {response.text}")
        return None

def get_departures(username: str, password: str, station_data: dict) -> dict:
    """Fragt die Abfahrtszeiten für eine bestimmte Station ab."""
    current_time = datetime.now()
    formatted_date = current_time.strftime("%d.%m.%Y")
    formatted_time = current_time.strftime("%H:%M")

    request_body = {
        "version": 59,
        "station": {
            "name": station_data["name"],
            "city": station_data["city"],
            "combinedName": station_data["combinedName"],
            "id": station_data["id"],
            "type": "STATION",
            "coordinate": station_data["coordinate"]
        },
        "time": {
            "date": formatted_date,
            "time": formatted_time
        },
        "maxList": 10,
        "maxTimeOffset": 200,
        "useRealtime": True
    }

    body = json.dumps(request_body)
    signature = create_signature(body, password)

    headers = {
        "Content-Type": "application/json",
        "geofox-auth-type": "HmacSHA1",
        "geofox-auth-user": username,
        "geofox-auth-signature": signature,
    }

    response = requests.post("https://gti.geofox.de/gti/public/departureList", headers=headers, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        LOGGER.error(f"HTTP Fehler bei getDepartures: {response.status_code}")
        LOGGER.error(f"Fehlerdetails: {response.text}")
        return None

def setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HVV Transport integration."""
    username = config[DOMAIN]["username"]
    password = config[DOMAIN]["password"]
    
    hass.states.set(DOMAIN + ".status", "online")

    def handle_get_departures(call):
        station_name = call.data.get('station_name')
        station_info = check_name(username, password, station_name)
        if station_info and station_info["returnCode"] == "OK":
            departures = get_departures(username, password, station_info["results"][0])
            if departures:
                hass.states.set(DOMAIN + ".departures", json.dumps(departures))

    hass.services.register(DOMAIN, 'get_departures', handle_get_departures)

    return True