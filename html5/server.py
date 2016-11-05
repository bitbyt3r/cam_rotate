#!/usr/bin/python3
import subprocess
import websockets
import threading
import random
import asyncio
import json
import time

speed = 1

def update(spd):
  global speed
  speed = spd

class cameraThread:
  def __init__(self, update):
    self.update = update
    self.thread = threading.Thread(target=self.run)
    self.image = {}
    self.speed = {}

  def start(self):
    self.thread.daemon = True
    self.thread.start()

  def run(self):
    while True:
      self.speed = random.random()
      self.update(self.speed)

cam = cameraThread(update)
cam.start()

async def open(websocket, path):
  print("Opened websocket at {}".format(path))
  myspeed = 0
  while True:
    if speed != myspeed:
      await websocket.send(json.dumps({'type': 'speed', 'speed': speed}))
      myspeed = speed
    await asyncio.sleep(0.15)

print("Serving websockets...")
ws_server = websockets.serve(open, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()
