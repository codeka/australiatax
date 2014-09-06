#!/bin/bash

APPSERVER=`which dev_appserver.py`
python2.7 $APPSERVER --host=0.0.0.0 --port=8246 \
        --automatic_restart --dev_appserver_log_level=debug \
        --enable_sendmail=true \
	web

