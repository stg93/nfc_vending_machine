#!/usr/bin/python3

import binascii
import sys
import Adafruit_PN532 as PN532

CS   = 8
MOSI = 10
MISO = 9
SCLK = 11

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

pn532.begin()

# Get the firmware version from the chip and print(it out.)
#ic, ver, rev, support = pn532.get_firmware_version()
#print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()

def getUID():
	print('Waiting for NFC chip...')
	while True:
		try:
			# Check if a card is available to read.
			uid = pn532.read_passive_target()
		except RuntimeError:
			return "-1"
		# Try again if no card is available.
		if uid is None:
			continue
		#print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
		uid = str(format(binascii.hexlify(uid)))
		return uid[2:-1]
