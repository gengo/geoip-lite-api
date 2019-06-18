## GeoIP lite API

API for MaxMind's [GeoLite2](https://dev.maxmind.com/geoip/geoip2/geolite2/) database.
This app retrieves the database from an s3 bucket and runs uwsgi to host the api built using [hug](https://www.hug.rest/)

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
hug -f api.py
```
Note: You must have the GeoLite2-City maxmind database in ```/srv``` directory.
