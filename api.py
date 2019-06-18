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
            # return info['subdivisions'][0]['']

            result = {
                "ip" : ipv4,
                "continent_code" : info['continent']['code'],
                "continent_name" : info['continent']['names']['en'],
                "country_code" : info['country']['iso_code'],
                "country_name" : info['country']['names']['en'],
                "region_code" : info['subdivisions'][0]['iso_code'],
                "region_name" : info['subdivisions'][0]['names']['en'],
                "city" : info['city']['names']['en'],
                "zip" : info['postal']['code'],
                "latitude" : info['location']['latitude'],
                "longitude" : info['location']['longitude'],
                "location" : {
                    "geonameid" : info['city']['geoname_id'],
                    "time_zone" : info['location']['time_zone']
                }
            }

            return result
        except ValueError:
            raise falcon.HTTPBadRequest('message', 'Invalid IPv4 address')


logging.info('Reading maxmind DB from {}'.format('path'))
start = time.process_time()
reader = maxminddb.open_database('/srv/GeoLite2-City.mmdb')
logging.info('Done. Took {}'.format(time.process_time() - start))

route = hug.route.API(__name__)
route.object('/')(GeoIP(reader))
