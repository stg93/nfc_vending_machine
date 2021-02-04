#!/usr/bin/python3

from functions import *

login = False

while not login:
	try:
		dbuser=input("Benutzername: ")
		dbpwd=input("Password: ")
		db = DB(dbuser,dbpwd)
		print("Anmeldung erfolgreich")
		login = True
	except:
		print("Anmeldung fehlgeschlagen")

id = input("ID: ")
id = int(id)
name = input("Name: ")

try:
	db.add_user(id, name)
	print("Datensatz angelegt")
except:
	print("Scheisse gelaufen")

db.close_db()
