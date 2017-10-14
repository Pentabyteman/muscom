#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import json
import socket_client

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic

class VotingClient(QMainWindow, socket_client.SocketClient):

    data_received = pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super(VotingClient, self).__init__(*args, **kwargs)
        self.data_received.connect(self.on_receive)
        
    def on_receive(self, query):
        print("receiving", query)
        datapackages = json.loads(query)
        print(datapackages)
        
    def upvote(self, song_id):
        text = '{"action":"upvote", "value":"' + song_id + '"}'
        self.send(text)
