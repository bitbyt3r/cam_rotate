#!/usr/bin/python
import ctypes
import time

drawLib = ctypes.cdll.LoadLibrary("./draw.so")
window = drawLib.CreateWindow()
drawLib.InitWindow(window)

i = ctypes.c_float()
i.value = 1

while True:
  time.sleep(1)
  drawLib.Draw(window, i)
  i.value += 1
