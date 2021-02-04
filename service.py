#!/usr/bin/python3

import sqlfunctions as sql
import readchip
import time
import sys
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import logging

def errorMessage(string):
    lcd.clear()
    lcd.message(string)
    for i in range(0, 3):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.2)
    time.sleep(1.8)
    lcd.clear()

def buy(pin):
    if pin == slot1:
        price = price_slot1
    elif pin == slot2:
        price = price_slot2
    else:
        errorMessage("Fehler bei\nden F\xE1chern")

    if used and not lowCredit:

        global credit
        global uid
        global name
        global remainingTime

        if credit < price:
            remainingTime = 4
            GPIO.output(activateSlots, GPIO.LOW)
            errorMessage("Zu wenig\nGuthaben")
            time.sleep(2)
            return

        credit = credit - price

        if credit < maxPrice:
            GPIO.output(activateSlots, GPIO.LOW)

        db.update_credit(uid, credit)
        credit_str = str(credit)
        lcd.clear()
        lcd.message(name + "\n" + credit_str)

    elif used and lowCredit:
        errorMessage("Zu wenig\nGuthaben")

    else:
        lcd.clear()
        lcd.message(str(price))
        t = 5
        while t > 0:
            t -= 1
            if used:
                return
            time.sleep(1)
        lcd.clear()

logging.basicConfig(filename="machine.log", format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)

lcd_rs = 20
lcd_en = 21
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18

buzzer = 13

slot1 = 26
slot2 = 16
activateSlots = 19

price_slot1 = 1.0
price_slot2 = 1.25
maxPrice = max(price_slot1, price_slot2)

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 16, 2)

GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

for elem in [slot1, slot2]:
    GPIO.setup(elem, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(elem, GPIO.FALLING, callback=buy, bouncetime=200)

GPIO.setup(activateSlots, GPIO.OUT)
GPIO.output(activateSlots, GPIO.LOW)

try:
    db = sql.DB("root", "sqlraspberrypi")
except:
    logging.critical("Login to SQL database failed")
    errorMessage("Fehler bei\nDatenbankanmeld.")
    lcd.message("Fehler bei\nDatenbankanmeld.")
    sys.exit()

used = False
lowCredit = False

try:
    while True:
        uid = readchip.getUID()

        print("Found UID: " + uid)

        data = db.get_data(uid)
        if data == None:
            logging.warning("Invalid UID found: %s",uid)
            errorMessage("Ung\xF5ltiger\nChip")
            continue

        used = True

        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(buzzer, GPIO.LOW)

        name = data[1]
        credit = data[2]

        logging.info("%s logged in with %s credit", name, credit)

        if credit < maxPrice:
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
            remainingTime -= 1
            time.sleep(1)

        lcd.clear()
        GPIO.output(activateSlots, GPIO.LOW)
        used = False
except:
    db.close_db()
    GPIO.cleanup()
    #traceback.print_exception()
    print("Service stopped")
    sys.exit()
