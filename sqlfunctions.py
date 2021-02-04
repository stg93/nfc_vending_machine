#!/usr/bin/python3

import pymysql

class DB():
	def __init__(self, usr, pwd):
		db = pymysql.connect(host="localhost", user=usr, passwd=pwd, db="machine")
		db.autocommit(True)
		self.cur = db.cursor()

	def close_db( self ):
		self.cur.close()

	def add_user(self,uid,name,credit):
		add=self.cur.execute("INSERT INTO users (uid, name, credit) VALUES (%s,%s,%s)", (uid, name, credit))

	def get_data(self,uid):
		self.cur.execute("SELECT * FROM users WHERE uid=%s", uid)
		data=self.cur.fetchone()
		return data

	def update_credit(self,uid,credit):
		self.cur.execute("UPDATE users SET credit = %s WHERE uid = %s", (credit,uid))
