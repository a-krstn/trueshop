#!/bin/sh
sleep 10
celery --broker=redis://shop_cache:6379 flower