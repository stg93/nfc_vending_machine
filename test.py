#!/usr/bin/python3

import sys
import logging
import time
import readchip

logging.basicConfig(filename="test.log", format="%(asctime)s %(message)s", level=logging.DEBUG)

logging.info("started")

time.sleep(3)

logging.info("ended")

