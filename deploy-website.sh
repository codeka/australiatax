#!/bin/bash

# update the RESOURCE_VERSION in the file handlers/__init__.py so that
# all our resource references go to a different file. This is our cache-busting
# mechanism.
sed -r 's/(RESOURCE_VERSION\s*=\s*)([0-9]+)/echo \1$((\2+1))/ge' web/handlers/__init__.py > /tmp/australiatax.txt
mv /tmp/australiatax.txt web/handlers/__init__.py

# now do the actual upload.
APPCFG=`which appcfg.py`
python2.7 $APPCFG --oauth2 update web


