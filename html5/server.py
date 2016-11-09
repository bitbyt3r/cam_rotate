#!/usr/bin/python3
import subprocess
import websockets
import threading
import asyncio
import serial
import random
import json
import time

speed = 1
avgspeed = 0

def update(spd):
  global speed, avgspeed
  speed = spd * -1
  speed = max(-1, min(1, (speed / 150)))
  avgspeed *= 0.9
  avgspeed += speed*0.1
  print("New speed: {}".format(avgspeed))
  with open("/tmp/pitch", "w") as PITCHFH:
    PITCHFH.write(str(avgspeed))

class cameraThread:
  def __init__(self, update):
    self.update = update
    self.thread = threading.Thread(target=self.run)
    self.ser = serial.Serial()
    self.ser.baudrate = 115200
    self.ser.port = '/dev/ttyUSB0'
    self.ser.open()
    self.speed = {}

  def start(self):
    self.thread.daemon = True
    self.thread.start()

  def run(self):
    while True:
      try:
        line = self.ser.readline().decode('ASCII')
        self.speed = line.split("READ:")[1]
        self.speed.strip()
        self.update(int(self.speed))
      except:
        print("Could not parse serial command.")

cam = cameraThread(update)
cam.start()

async def openwebsocket(websocket, path):
  print("Opened websocket at {}".format(path))
  myspeed = 0
  while True:
    if avgspeed != myspeed:
      await websocket.send(json.dumps({'type': 'speed', 'speed': avgspeed}))
      myspeed = avgspeed
    await asyncio.sleep(0.15)

print("Serving websockets...")
ws_server = websockets.serve(openwebsocket, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()
