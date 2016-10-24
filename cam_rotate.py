#!/usr/bin/python
import os
import glob
import json
import ctypes
import time
import usb
import server

drawLib = ctypes.cdll.LoadLibrary("./draw.so")
window = drawLib.CreateWindow()
drawLib.InitWindow(window)

i = ctypes.c_float()
i.value = 1

config = {}

speed = 0
musicavg = 0

def speed_callback(num):
  global speed
  global musicavg
  if 'check' in config.keys():
    if 'reverse' in config['check']:
      num *= -1
  max_step = 6.282 / float(config['fpr'][0])
  scaled = (num / float(config['maxspeed'][0])) * max_step
  musicspeed = max(-1, min(1, (num / float(config['maxspeed'][0]))))
  musicavg *= 0.9
  musicavg += musicspeed*0.1
  scaled = max(scaled, max_step*-1)
  scaled = min(scaled, max_step)
  speed = speed*0.5
  speed += scaled*0.5
  with open("/tmp/pitch", "w") as PITCHFH:
    PITCHFH.write(str(musicavg))

def config_callback(configuration):
  print("Updating config")
  global config
  config = dict(configuration)
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

with open("/tmp/pitch", "w") as PITCHFH:
  PITCHFH.write("0.0")

mounter = usb.USBDriveMounter()
mounter.start_monitor()
mounter.mount_all()

song = ''

for filename in glob.iglob('/mnt/**', recursive=True):
  print(filename)
  if "wav" in filename or "mp3" in filename:
    song = os.path.join('/mnt', filename)
if song:
  os.system("xwax -a default -p {} &".format(song))
else:
  os.system("xwax -a default -p {} &".format('/home/mark25/test.wav'))

while True:
  time.sleep(1/float(config['fps'][0]))
  i.value += speed
  drawLib.Draw(window, i)
  if mounter.poll_changes():
    song = ''
    mounter.mount_all()
    os.system("pkill xwax")
    for filename in glob.iglob('/mnt/**', recursive=True):
      print(filename)
      if "wav" in filename or "mp3" in filename:
        song = os.path.join('/mnt', filename)
    if song:
      os.system("xwax -a default -p {} &".format(song))
    else:
      os.system("xwax -a default -p {} &".format('/home/mark25/test.wav'))
