"""
Weather information for air and road temperature, provided by Trafikverket.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.trafikverket_weatherstation/
"""
import json
import logging
from datetime import timedelta
import requests

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, ATTR_ATTRIBUTION, TEMP_CELSIUS, CONF_API_KEY, CONF_TYPE)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "Data provided by Trafikverket API"

CONF_STATION = 'station'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)
SCAN_INTERVAL = timedelta(seconds=300)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_STATION): cv.string,
    vol.Required(CONF_TYPE): vol.In(['air', 'road']),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    sensor_name = config.get(CONF_NAME)
    sensor_api = config.get(CONF_API_KEY)
    sensor_station = config.get(CONF_STATION)
    sensor_type = config.get(CONF_TYPE)

    add_devices([TrafikverketWeatherStation(
        sensor_name, sensor_api, sensor_station, sensor_type)], True)


class TrafikverketWeatherStation(Entity):
    """Representation of a Sensor."""

    def __init__(self, sensor_name, sensor_api, sensor_station, sensor_type):
        """Initialize the sensor."""
        self._name = sensor_name
        self._api = sensor_api
        self._station = sensor_station
        self._type = sensor_type
        self._state = None
        self._attributes = {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        url = 'http://api.trafikinfo.trafikverket.se/v1.3/data.json'

        if self._type == 'road':
            air_vs_road = 'Road'
        else:
            air_vs_road = 'Air'

        xml = """
        <REQUEST>
              <LOGIN authenticationkey='""" + self._api + """' />
              <QUERY objecttype="WeatherStation">
                    <FILTER>
                          <EQ name="Name" value='""" + self._station + """' />
                    </FILTER>
                    <INCLUDE>Measurement.""" + air_vs_road + """.Temp</INCLUDE>
              </QUERY>
        </REQUEST>"""

        # Testing JSON post request.
        try:
            post = requests.post(url, data=xml.encode('utf-8'), timeout=5)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("Please check network connection: %s", err)
            return None

        # Checking JSON respons.
        try:
            # loa (load) = loaded json
            loa = json.loads(post.text)

            # mea = measurement
            mea = loa["RESPONSE"]["RESULT"][0]

            # wea = weather station
            wea = mea["WeatherStation"][0]["Measurement"]
        except KeyError:
            _LOGGER.error("Incorrect weather station or API key.")
            return None

        # air_vs_road contains "Air" or "Road" depending on user input.
        self._state = wea[air_vs_road]["Temp"]
