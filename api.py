import hug
import falcon
import maxminddb
import time
import logging

class GeoIP:
    def __init__(self, reader):
        self.reader = reader

    @hug.object.get(urls='/geoip/{ipv4}')
    def get(self, ipv4: str):
        try:
            info = self.reader.get(ipv4)

            result = {
                "ip" : ipv4,
                "continent_code" : "",
                "continent_name" : "",
                "country_code" : "",
                "country_name" : "",
                "region_code" : "",
                "region_name" : "",
                "city" : "",
                "zip" : "",
                "latitude" : "",
                "longitude" : "",
                "location" : {
                    "geonameid" : "",
                    "time_zone" : ""
                }
            }

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
        except ValueError:
            raise falcon.HTTPBadRequest('message', 'Invalid IPv4 address')


logging.info('Reading maxmind DB from {}'.format('path'))
start = time.process_time()
reader = maxminddb.open_database('/srv/GeoLite2-City.mmdb')
logging.info('Done. Took {}'.format(time.process_time() - start))

route = hug.route.API(__name__)
route.object('/')(GeoIP(reader))
