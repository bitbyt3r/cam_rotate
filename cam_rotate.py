#!/usr/bin/python
import json
import ctypes
import time
import server

drawLib = ctypes.cdll.LoadLibrary("./draw.so")
window = drawLib.CreateWindow()
drawLib.InitWindow(window)

i = ctypes.c_float()
i.value = 1

config = {}

speed = 0

def speed_callback(num):
  global speed
  if 'check' in config.keys():
    if 'reverse' in config['check']:
      num *= -1
  max_step = 6.282 / float(config['fpr'][0])
  scaled = (num / float(config['maxspeed'][0])) * (6.282 / float(config['fpr'][0]))
  speed = speed*0.5
  speed += scaled*0.5

def config_callback(configuration):
  print("Updating config")
  global config
  config.update(configuration)
  print(config)
  scale = ctypes.c_float()
  scale.value = float(config['scale'][0])
  icx = ctypes.c_float()
  icx.value = float(config['icx'][0])
  icy = ctypes.c_float()
  icy.value = float(config['icy'][0])
  scx = ctypes.c_float()
  scx.value = float(config['scx'][0])
  scy = ctypes.c_float()
  scy.value = float(config['scy'][0])
  drawLib.Config(window, scale, icx, icy, scx, scy)

speedServer = server.SpeedServer(speed_callback)
configServer = server.ConfigServer(config_callback)

while True:
  time.sleep(1/float(config['fps'][0]))
  i.value += speed
  drawLib.Draw(window, i)
