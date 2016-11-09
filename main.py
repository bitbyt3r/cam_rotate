import time
import socket
import machine
import esp

time.sleep(2)

adc = machine.ADC(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
  time.sleep(0.001)
  reading = adc.read()
  reading = reading - 289
  if abs(reading) < 2:
    reading = 0
  print("READ:{}".format(reading))
  host = "192.168.5.1"
  port = 8080
  sock.sendto("{}".format(reading), (host, port))
