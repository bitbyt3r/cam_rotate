#!/usr/bin/python
import socket
import threading

class SpeedServer:
  def __init__(self, callback):
    self.callback = callback
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    self.s = socket.socket()
    self.s.bind(addr)
    self.s.listen(1)
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()
    print("Started speed server thread.")

  def run(self):
    print("Running speed server")
    while True:
      try:
        cl, addr = self.s.accept()
        num = float(cl.recv(100))
        cl.close()
        self.callback(num)
      except:
        pass
