import hug
import html
import falcon
import logging
import maxminddb
import time
import os

import geoip2.webservice
from geoip2.errors import GeoIP2Error


GEOIP2_USER_ID = os.getenv('GEOIP2_USER_ID', '')
GEOIP2_LICENSE_KEY = os.getenv('GEOIP2_LICENSE_KEY', '')
GEOIP_SERVICE = 2

result = {
    'ip' : '',
    'continent_code' : '',
    'continent_name' : '',
    'country_code' : '',
    'country_name' : '',
    'region_code' : '',
    'region_name' : '',
    'city' : '',
    'zip' : '',
    'latitude' : '',
    'longitude' : '',
    'location' : {
        'geonameid' : '',
        'time_zone' : ''
    }
}


class GeoIP:
    def __init__(self, reader: None):
        self.reader = reader

    @hug.object.get(urls='/geoip/{ipv4}')
    def get(self, ipv4: str):
        result['ip'] = ipv4
        if GEOIP_SERVICE == 1:
            try:
                info = self.reader.get(ipv4)
            except ValueError:
                raise falcon.HTTPBadRequest('message', 'Invalid IPv4 address')

        else:
            client = geoip2.webservice.Client(
                GEOIP2_USER_ID,
                GEOIP2_LICENSE_KEY,
            )
            try:
                response = client.insights(ipv4)

                result['region_code'] =  self._text_escaper(response.subdivisions[0].iso_code)
                result['region_name'] = self._text_escaper(response.subdivisions[0].names['en'])
                result['city'] = self._text_escaper(response.city.names['en'])
                result['location']['geonameid'] = self._text_escaper(response.city.names['en'])
                result['zip'] = self._text_escaper(response.postal.code)
                result['continent_code'] = self._text_escaper(response.continent.code)
                result['continent_name'] = self._text_escaper(response.continent.names['en'])
                result['country_code'] = self._text_escaper(response.country.iso_code)
                result['country_name'] = self._text_escaper(response.country.names['en'])
                result['latitude'] = response.location.latitude
                result['longitude'] = response.location.longitude
                result['location']['time_zone'] = self._text_escaper(response.location.time_zone)

            except GeoIP2Error as error:
                logging.error(error)
                raise falcon.HTTPBadRequest('message', 'Invalid IPv4 address')

        if GEOIP_SERVICE == 1:
            if 'subdivisions' in info:
                result['region_code'] = info['subdivisions'][0]['iso_code']
                result['region_name'] = info['subdivisions'][0]['names']['en']

            if 'city' in info:
                result['city'] = info['city']['names']['en']
                result['location']['geonameid'] = info['city']['geoname_id']

            if 'postal' in info:
                result['zip'] = info['postal']['code']

            if 'continent' in info:
                result['continent_code'] = info['continent']['code']
                result['continent_name'] = info['continent']['names']['en']

            if 'country' in info:
                result['country_code'] = info['country']['iso_code']
                result['country_name'] = info['country']['names']['en']

            if 'location' in info:
                result['latitude'] = info['location']['latitude']
                result['longitude'] = info['location']['longitude']
                result['location']['time_zone'] = info['location']['time_zone']

        return result

    def _text_escaper(self, text: None):
        return html.escape(text, quote=True) if text else ''


logging.info('Reading maxmind DB from {}'.format('path'))
start = time.process_time()

if GEOIP_SERVICE == 1:
    reader = maxminddb.open_database('/srv/GeoLite2-City.mmdb')

logging.info('Done. Took {}'.format(time.process_time() - start))
route = hug.route.API(__name__)

if GEOIP_SERVICE == 1:
    route.object('/')(GeoIP(reader))
else:
    route.object('/')(GeoIP(''))
