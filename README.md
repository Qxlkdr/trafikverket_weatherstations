# Trafikverket WeatherStation

Showing weather information for air and road temperature provided by Trafikverket in Sweden. This Python file should be used as a custom component in Home Assistant.

#### Configuration
To enable this sensor, add the following lines to your `configuration.yaml`.

```
sensor:
  - platform: trafikverket_weatherstation
    name: Trafikverket Road WeatherStation Kungälv
    api_key: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Kungälv
    type: road
```

Configuration variables:

- **name** (*Required*): Unique name of the device in the frontend.
- **api_key** (*Required*): API key from Trafikverket
- **station** (*Required*): Name of the weather station
- **type** (*Required*): Defines which temperature you want (`air` or `road`)
- **scan_interval** (*Optional*): How frequently to query for new data (in seconds). Defaults to 300 seconds (5 minutes)

##### Getting API key:
[https://api.trafikinfo.trafikverket.se/](https://api.trafikinfo.trafikverket.se/)

##### See Trafikverket weather stations
[https://www.trafikverket.se/trafikinformation/vag/?TrafficType=personalTraffic&map=1/606442.17/6886316.22/&Layers=RoadWeather%2b](https://www.trafikverket.se/trafikinformation/vag/?TrafficType=personalTraffic&map=1/606442.17/6886316.22/&Layers=RoadWeather%2b)

##### Example

```
sensor:
  - platform: trafikverket_weatherstation
    name: Trafikverket Road WeatherStation Kungälv
    api_key: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Kungälv
    type: road
  - platform: trafikverket_weatherstation
    name: Trafikverket Air WeatherStation Lanna
    api_key: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Lanna
    type: air
    scan_interval: 600
```

*A good practice is to use `secrets.yaml` for all your API keys, username and password. You can read more about secrets [here](https://home-assistant.io/docs/configuration/secrets/).*