#!/usr/bin/python
import ctypes
import time
import server

drawLib = ctypes.cdll.LoadLibrary("./draw.so")
window = drawLib.CreateWindow()
drawLib.InitWindow(window)

i = ctypes.c_float()
i.value = 1
lasti = 0
max_step = 6.282 / 24

def callback(num):
  global i
  scaled = (num / 25) * (6.282 / 24)
  i.value = min(lasti + max_step, i.value + scaled)

speedServer = server.SpeedServer(callback)

while True:
  time.sleep(0.03)
  drawLib.Draw(window, i)
  lasti = i.value
