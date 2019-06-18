## GeoIP lite API

API for MaxMind's [GeoLite2](https://dev.maxmind.com/geoip/geoip2/geolite2/) database.
This downloads the database from an s3 bucket and runs uwsgi to host the API built using [hug](https://www.hug.rest/)

### To Run
```sh
cd geoip-lite-api
```
```sh
./run.sh [s3-path-for-geolite2]
```

### Development
Run
```sh
hug -f api.py -p 10000
```
Note: You must have the GeoLite2-City maxmind database in ```/srv``` directory.

### Usage
- ```/geoip/{ipv4}```

Example:
```sh
$ curl localhost:10000/geoip/8.8.8.8 | jq
{
  "continent": {
    "code": "NA",
    "geoname_id": 6255149,
    "names": {
      "de": "Nordamerika",
      "en": "North America",
      "es": "Norteamérica",
      "fr": "Amérique du Nord",
      "ja": "北アメリカ",
      "pt-BR": "América do Norte",
      "ru": "Северная Америка",
      "zh-CN": "北美洲"
    }
  },
  "country": {
    "geoname_id": 6252001,
    "iso_code": "US",
    "names": {
      "de": "USA",
      "en": "United States",
      "es": "Estados Unidos",
      "fr": "États-Unis",
      "ja": "アメリカ合衆国",
      "pt-BR": "Estados Unidos",
      "ru": "США",
      "zh-CN": "美国"
    }
  },
  "location": {
    "accuracy_radius": 1000,
    "latitude": 37.751,
    "longitude": -97.822,
    "time_zone": "America/Chicago"
  },
  "registered_country": {
    "geoname_id": 6252001,
    "iso_code": "US",
    "names": {
      "de": "USA",
      "en": "United States",
      "es": "Estados Unidos",
      "fr": "États-Unis",
      "ja": "アメリカ合衆国",
      "pt-BR": "Estados Unidos",
      "ru": "США",
      "zh-CN": "美国"
    }
  }
}
```
