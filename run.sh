#!/bin/sh -e
if [ $# -ne 1 ]; then
    CMDNAME=`basename $0`
    echo "Usage: $CMDNAME s3_path"
    exit 1
fi

S3_PATH=$1
FILENAME="GeoLite2-City.mmdb"
aws s3 cp $S3_PATH /srv/$FILENAME || exit 1

uwsgi --http 0.0.0.0:10000 --wsgi-file api.py --callable __hug_wsgi__
