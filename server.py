#!/usr/bin/python
import json
import socket
from flask import Flask, send_from_directory, request, render_template
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

class ConfigServer:
  def __init__(self, callback):
    self.callback = callback
    try:
      self.settings = self.readsettings("./settings.json")
    except:
      self.settings = {"icx": ["0.5"], "scy": ["0.5"], "fpr": ["24"], "scale": ["1"], "fps": ["30"], "icy": ["0.5"], "maxspeed": ["50"], "scx": ["0.5"], "check": [""]}
      self.writeback("./settings.json")
    self.callback(self.settings)
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()
    print("Started config server thread.")

  def run(self):
    print("Running config server")
    app = Flask(__name__, template_folder="./html")

    @app.route("/", methods=['GET', 'POST'])
    def index():
      if request.method == 'POST':
        self.writeback("./settings.json", values=request.form)
        self.callback(request.form)
      return render_template("index.html", data=self.settings)

    app.run(host="0.0.0.0", port=80, threaded=True)

  def readsettings(self, path):
    with open(path, "r") as FH:
      return json.loads(FH.read())

  def writeback(self, path, values={}):
    self.settings.update(values)
    with open(path, "w") as FH:
      FH.write(json.dumps(self.settings))
