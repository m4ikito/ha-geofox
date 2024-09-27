import requests
import json
from datetime import datetime
import hashlib
import hmac
import base64

class GeofoxAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://gti.geofox.de/gti"

    def create_signature(self, body):
        message = body.encode('utf-8')
        secret = self.password.encode('utf-8')
        signature = hmac.new(secret, message, hashlib.sha1).digest()
        return base64.b64encode(signature).decode()

    async def get_connection(self, station_start, station_dest):
        request_body = {
            "version": 59,
            "start": {
                "name": station_start,
                "type": "STATION"
            },
            "dest": {
                "name": station_dest,
                "type": "STATION"
            },
            "time": {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "time": datetime.now().strftime("%H:%M")
            },
            "timeIsDeparture": True,
            "realtime": "REALTIME"
        }

        body = json.dumps(request_body)
        signature = self.create_signature(body)

        headers = {
            "Content-Type": "application/json",
            "geofox-auth-type": "HmacSHA1",
            "geofox-auth-user": self.username,
            "geofox-auth-signature": signature,
        }

        response = requests.post(f"{self.base_url}/public/getRoute", headers=headers, data=body)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    async def get_route(self, station_start, station_dest):
        request_body = {
            "version": 59,
            "start": {
                "name": station_start,
                "type": "STATION"
            },
            "dest": {
                "name": station_dest,
                "type": "STATION"
            },
            "time": {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "time": datetime.now().strftime("%H:%M")
            },
            "timeIsDeparture": True,
            "realtime": "REALTIME"
        }

        body = json.dumps(request_body)
        signature = self.create_signature(body)

        headers = {
            "Content-Type": "application/json",
            "geofox-auth-type": "HmacSHA1",
            "geofox-auth-user": self.username,
            "geofox-auth-signature": signature,
        }

        response = requests.post(f"{self.base_url}/public/getRoute", headers=headers, data=body)

        if response.status_code == 200:
            return response.json()
        else:
            return None