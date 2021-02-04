#!/usr/bin/python3

from functions import *
from readchip import *
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import threading

lcd_rs		= 20
lcd_en		= 21
lcd_d4		= 25
lcd_d5		= 24
lcd_d6		= 23
lcd_d7		= 18
lcd_backlight	= 4

slot1		= 26
activateSlots	= 19

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 16, 2, lcd_backlight)

GPIO.setup(slot1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(activateSlots, GPIO.OUT)
GPIO.output(activateSlots, GPIO.LOW)

class userThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.stopFlag = False
	def run(self,uid):
		print("Found UID: " + uid)

		data=db.getData(uid)
		if data == None:
			print("Invalid UID found")
			return
		used=True
		name = data[1]
		credit = data[2]
		if credit < 1:
			lowCredit = True
		else:
			lowCredit = False
		credit_str = str(data[2])
		lcd.clear()
		lcd.message(name + "\n" + credit_str)
		if not lowCredit:
			GPIO.output(activateSlots, GPIO.HIGH)
		remainingTime = 10
		while remainingTime > 0:
			if self.stopFlag:
				sys.exit()
			remainingTime -= 1
			time.sleep(1)
		lcd.clear()
		GPIO.output(activateSlots, GPIO.LOW)
		used=False
	def stop(self):
		self.stopFlag = True

try:
	db = DB("root","sqlraspberrypi")
	print("Access to SQL database granted")
except:
	print("Login to SQL database failed")

used = False
lowCredit = False

def buy(pin):
	if used and not lowCredit:
		global credit
		global uid
		#global credit_str
		global name
		global remainingTime

		if credit < 1:
			remainingTime = 5
			lcd.clear()
			lcd.message("Zu wenig\nGuthaben")
			GPIO.output(activateSlots, GPIO.LOW)
			time.sleep(5)
			return
		credit = credit - 1
		if credit < 1:
			GPIO.output(activateSlots, GPIO.LOW)
		#print(uid + " hat " + credit_str + " - 1 = " + str(credit))
		db.update_credit(uid,credit)
		credit_str=str(credit)
		lcd.clear()
		lcd.message(name + "\n" + credit_str)
	elif used and lowCredit:
		lcd.clear()
		lcd.message("Zu wenig\nGuthaben")
	else:
		lcd.clear()
		lcd.message("1.00")
		t = 5
		while t > 0:
			t -= 1
			if used:
				return
			time.sleep(1)			
		lcd.clear()	

GPIO.add_event_detect(slot1, GPIO.FALLING, callback=buy, bouncetime=200)

def newUser(uid):
	print("Found UID: " + uid)

	data=db.getData(uid)
	if data == None:
		print("Invalid UID found")
		return
	used=True
	name = data[1]
	credit = data[2]
	if credit < 1:
		lowCredit = True
	else:
		lowCredit = False
	credit_str = str(data[2])
	lcd.clear()
	lcd.message(name + "\n" + credit_str)
	if not lowCredit:
		GPIO.output(activateSlots, GPIO.HIGH)
	remainingTime = 10
	while remainingTime > 0:
#		if self.stopFlag = True:
#			sys.exit()
		remainingTime -= 1
		time.sleep(1)
	lcd.clear()
	GPIO.output(activateSlots, GPIO.LOW)
	used=False

lastUID = "0"
CurrentThread = None

try:
	while True:
#		try:
		uid = getUID()
#		except RuntimeError:
#			Print("Invalid UID found")
#			continue
		if uid != lastUID:
			newThread = userThread()
			if currentThread != None:
				currentThread.stop()	
				currentThread.join()
			lastUID = uid
			currentThread = newThread
			currentThread.start(uid)
except:
	db.close_db()
	GPIO.cleanup()
#	traceback.print_exception()
	print("Service stopped")
	sys.exit()
