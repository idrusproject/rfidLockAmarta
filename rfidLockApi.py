# username : pi
# pass     : raspberry136
import RPi.GPIO as io
import paho.mqtt.client as mqtt
from mfrc522 import SimpleMFRC522
from gpiozero import Button
import requests
import json
import time

client = mqtt.Client()

io.setmode(io.BCM)
io.setwarnings(False)
rLed = 26
gLed = 19
bLed = 13
lock = 5
buzzer = 6
exitButton = 16

io.setup(rLed, io.OUT)
io.setup(gLed, io.OUT)
io.setup(bLed, io.OUT)
io.setup(buzzer, io.OUT)
io.setup(lock, io.OUT)
exitBtn = Button(exitButton)
io.output(rLed, 1)
io.output(gLed, 1)
io.output(bLed, 1)
io.output(lock, 1)
io.output(buzzer, 0)

myTimes = 0
myCard = "xxx"
timeLock = 3
timeBtn = 3

reader = SimpleMFRC522()

headers = {"X-API-KEY": "NchPCPeiWk7fma8oXSjNO7XZ2bGCv9f148XHyKlS"}
url = "https://j5michmb2l.execute-api.ap-southeast-1.amazonaws.com/v1/validate"

# r = requests.post(url, params={"SK" : "476E5209-E443-4CF3-843A-20648CCCBE6C","CardId": "B8EFD03D-C2EC-4559-C43B-08D9FFF4FD00"}, headers=headers)

print("Program Ready To Use")
time.sleep(0.9)
print("Time now : " + time.ctime(time.time()))


while True:
    myCard = ""
    if (time.time() - myTimes > 3):
        io.output(rLed, 0)
        time.sleep(0.1)
        io.output(rLed, 1)
        myTimes = time.time()

    #id, text = reader.read()
    #myCard = str(id)

    text = reader.read_id_no_block()
    myCard = str(text)
    #print (myCard)
    #print (len(myCard))

    #print (exitBtn)
    if (exitBtn.is_pressed):
        print("Button Pressed")
        myTimes = time.time()
        while (exitBtn.is_pressed):
            time.sleep(0.1)
            if (time.time() - myTimes > timeBtn):
                print("Open By Exit Button")
                io.output(gLed, 0)
                io.output(buzzer, 1)
                time.sleep(0.1)
                io.output(gLed, 1)
                io.output(buzzer, 0)
                time.sleep(0.1)
                io.output(gLed, 0)
                io.output(buzzer, 1)
                time.sleep(0.1)
                io.output(gLed, 1)
                io.output(buzzer, 0)
                io.output(lock, 0)
                time.sleep(timeLock)
                io.output(lock, 1)

    # if (len(myCard) > 4):
    if (myCard != "None"):
        print(myCard)
        io.output(bLed, 0)
        time.sleep(0.1)
        io.output(bLed, 1)
        if (myCard == "507554571747" or myCard == "585515753935" or myCard == "584186363956"):
            myCard = "B8EFD03D-C2EC-4559-C43B-08D9FFF4FD00"

        payload = {
            "CardId": myCard
        }
        print("HTTP Request")
        r = requests.post(url, headers=headers, json=payload)

        if r.status_code != 200:
            print("Error:", r.status_code)

        data = r.json()
        access = data["status"]
        print(access)

        if access == True:
            print("Access Granted")
            io.output(gLed, 0)
            io.output(buzzer, 1)
            time.sleep(0.1)
            io.output(gLed, 1)
            io.output(buzzer, 0)
            time.sleep(0.1)
            io.output(gLed, 0)
            io.output(buzzer, 1)
            time.sleep(0.1)
            io.output(gLed, 1)
            io.output(buzzer, 0)
            io.output(lock, 0)
            time.sleep(timeLock)
            io.output(lock, 1)
            client.connect("broker.hivemq.com", 1883, 60)
            client.publish("amarta136/doorlock", "Hello, World!")
            client.disconnect()
        else:
            print("Access Decline")
            io.output(rLed, 0)
            io.output(buzzer, 1)
            time.sleep(0.8)
            io.output(rLed, 1)
            io.output(buzzer, 0)
    time.sleep(0.2)
