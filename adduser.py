#!/usr/bin/python3

import sqlfunctions as sql
import readchip

try:
	db = sql.DB("root","sqlraspberrypi")
	print("Access to SQL database granted")
except:
	print("Login to SQL database failed")

uid = readchip.getUID()

print("Found UID: " + uid)

name = input("Name: ")
credit = input("Credit: ")
credit = float(credit)

try:
	db.add_user(uid, name, credit)
	print("New user saved")
except:
	print("Error creating new user")

db.close_db()
