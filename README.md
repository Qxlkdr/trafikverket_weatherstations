# Trafikverket WeatherStations

Showing weather information for air and road temperature provided by Trafikverket in Sweden. This Python file should be used as a custom component in Home Assistant.

#### Configuration
To enable this sensor, add the following lines to your `configuration.yaml`.

```
sensor:
  - platform: trafikverket_weatherstations
    name: Trafikverket Road WeatherStation Kungälv
    api: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Kungälv
    type: road
    unit_of_measurement: "°C"
```

Configuration variables:

- **name** (*Required*): Unique name of the device in the frontend.
- **api** (*Required*): API key from Trafikverket
- **station** (*Required*): Name of the weather station
- **type** (*Required*): Defines which temperature you want (`air` or `road`)

##### Getting API key:
[https://api.trafikinfo.trafikverket.se/](https://api.trafikinfo.trafikverket.se/)

##### See Trafikverket weather stations
[https://www.trafikverket.se/trafikinformation/vag/?TrafficType=personalTraffic&map=1/606442.17/6886316.22/&Layers=RoadWeather%2b](https://www.trafikverket.se/trafikinformation/vag/?TrafficType=personalTraffic&map=1/606442.17/6886316.22/&Layers=RoadWeather%2b)

##### Example

```
sensor:
  - platform: trafikverket_weatherstations
    name: Trafikverket Road WeatherStation Kungälv
    api: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Kungälv
    type: road
    unit_of_measurement: "°C"
  - platform: trafikverket_weatherstations
    name: Trafikverket Air WeatherStation Lanna
    api: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX
    station: Lanna
    type: air
    unit_of_measurement: "°C"
```

A good practice is to use secrets.yaml for all your API keys, username and password. Below is an example of using secrets.yaml for your Trafikverket API key.

```
## secrets.yaml
trafikvarketapi: eXXcbXXXacXXXXc39XX3aXXX4aXX46XX

## configuration.yaml
  - platform: trafikverket_weatherstations
    name: Trafikverket Air WeatherStation Lanna
    api: !secret trafikvarketapi
    station: Lanna
    type: air
    unit_of_measurement: "°C"
