import html
import logging
import os
import time

import falcon
import geoip2.webservice
import hug
import maxminddb
from geoip2.errors import GeoIP2Error

GEOIP2_USER_ID = os.getenv("GEOIP2_USER_ID", "")
GEOIP2_LICENSE_KEY = os.getenv("GEOIP2_LICENSE_KEY", "")
NON_PAID_VERSION = 1
PAID_VERSION = 2
GEOIP_SERVICE = PAID_VERSION

result = {
    "ip": "",
    "continent_code": "",
    "continent_name": "",
    "country_code": "",
    "country_name": "",
    "region_code": "",
    "region_name": "",
    "city": "",
    "zip": "",
    "latitude": "",
    "longitude": "",
    "location": {"geonameid": "", "time_zone": ""},
}


class GeoIP:
    @hug.object.get(urls="/geoip/{ipv4}")
    def get(self, ipv4: str):
        if GEOIP_SERVICE == NON_PAID_VERSION:
            return self._get_geoip2_service(ipv4)
        else:
            return self._get_geoip_service(ipv4)

    def _get_geoip_service(self, ipv4: str):
        reader = maxminddb.open_database("/srv/GeoLite2-City.mmdb")
        try:
            info = reader.get(ipv4)
        except ValueError:
            raise falcon.HTTPBadRequest("message", "Invalid IPv4 address")

        result["ip"] = ipv4

        if "subdivisions" in info:
            result["region_code"] = info["subdivisions"][0]["iso_code"]
            result["region_name"] = info["subdivisions"][0]["names"]["en"]

        if "city" in info:
            result["city"] = info["city"]["names"]["en"]
            result["location"]["geonameid"] = info["city"]["geoname_id"]

        if "postal" in info:
            result["zip"] = info["postal"]["code"]

        if "continent" in info:
            result["continent_code"] = info["continent"]["code"]
            result["continent_name"] = info["continent"]["names"]["en"]

        if "country" in info:
            result["country_code"] = info["country"]["iso_code"]
            result["country_name"] = info["country"]["names"]["en"]

        if "location" in info:
            result["latitude"] = info["location"]["latitude"]
            result["longitude"] = info["location"]["longitude"]
            result["location"]["time_zone"] = info["location"]["time_zone"]

        return result

    def _get_geoip2_service(self, ipv4: str):
        client = geoip2.webservice.Client(GEOIP2_USER_ID, GEOIP2_LICENSE_KEY)
        try:
            response = client.insights(ipv4)
            result["ip"] = ipv4
            result["region_code"] = self._escape_text(response.subdivisions[0].iso_code)
            result["region_name"] = self._escape_text(
                response.subdivisions[0].names["en"]
            )
            result["city"] = self._escape_text(response.city.names["en"])
            result["location"]["geonameid"] = self._escape_text(
                response.city.names["en"]
            )
            result["zip"] = self._escape_text(response.postal.code)
            result["continent_code"] = self._escape_text(response.continent.code)
            result["continent_name"] = self._escape_text(response.continent.names["en"])
            result["country_code"] = self._escape_text(response.country.iso_code)
            result["country_name"] = self._escape_text(response.country.names["en"])
            result["latitude"] = response.location.latitude
            result["longitude"] = response.location.longitude
            result["location"]["time_zone"] = self._escape_text(
                response.location.time_zone
            )

        except GeoIP2Error as error:
            logging.error(error)
            raise falcon.HTTPBadRequest("message", "Invalid IPv4 address")
        return result

    def _escape_text(self, text: None):
        return html.escape(text, quote=True) if text else ""


logging.info("Reading maxmind DB from {}".format("path"))
start = time.process_time()
logging.info("Done. Took {}".format(time.process_time() - start))
route = hug.route.API(__name__)
route.object("/")(GeoIP())
