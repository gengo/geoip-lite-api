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
            return self.reader.get(ipv4)
        except ValueError:
            raise falcon.HTTPBadRequest('message', 'Invalid IPv4 address')


logging.info('Reading maxmind DB from {}'.format('path'))
start = time.process_time()
reader = maxminddb.open_database('/srv/GeoLite2-City.mmdb')
logging.info('Done. Took {}'.format(time.process_time() - start))

route = hug.route.API(__name__)
route.object('/')(GeoIP(reader))
