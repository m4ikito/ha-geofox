from homeassistant.helpers import discovery
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

DOMAIN = "hvv_transport"
CONF_STATION_NAME_START = "station_name_start"
CONF_STATION_NAME_DEST = "station_name_dest"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_STATION_NAME_START): cv.string,
        vol.Required(CONF_STATION_NAME_DEST): cv.string
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    """Set up the HVV Transport component."""
    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    station_start = config[DOMAIN][CONF_STATION_NAME_START]
    station_dest = config[DOMAIN][CONF_STATION_NAME_DEST]

    hass.data[DOMAIN] = {
        CONF_USERNAME: username,
        CONF_PASSWORD: password,
        CONF_STATION_NAME_START: station_start,
        CONF_STATION_NAME_DEST: station_dest
    }

    await discovery.async_load_platform(hass, "sensor", DOMAIN, {}, config)

    return True