from homeassistant.components.sensor import SensorEntity
from .api import GeofoxAPI
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    data = hass.data["hvv_transport"]
    username = data[CONF_USERNAME]
    password = data[CONF_PASSWORD]
    station_start = data["station_name_start"]
    station_dest = data["station_name_dest"]

    api = GeofoxAPI(username, password)

    sensors = [
        HVVTransportSensor(api, station_start, station_dest, "connection"),
        HVVTransportSensor(api, station_start, station_dest, "station_name"),
        HVVTransportSensor(api, station_start, station_dest, "route"),
    ]

    async_add_entities(sensors, True)

class HVVTransportSensor(SensorEntity):
    def __init__(self, api, station_start, station_dest, sensor_type):
        self.api = api
        self.station_start = station_start
        self.station_dest = station_dest
        self.sensor_type = sensor_type
        self._state = None

    @property
    def name(self):
        return f"hvv_transport_{self.sensor_type}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        if self.sensor_type == "connection":
            data = await self.api.get_connection(self.station_start, self.station_dest)
            self._state = data.get("next_departure")
        elif self.sensor_type == "station_name":
            self._state = self.station_start
        elif self.sensor_type == "route":
            data = await self.api.get_route(self.station_start, self.station_dest)
            self._state = data.get("route_description")