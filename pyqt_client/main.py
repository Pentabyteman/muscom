#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import json
import socket_client
import itertools

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic

class VotingClient(QMainWindow, socket_client.SocketClient):

    data_received = pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super(VotingClient, self).__init__(*args, **kwargs)
        self.data_received.connect(self.on_receive)
        uic.loadUi('muscom.ui', self)
        self.lastvote = ""
        self.show()
        self.connect("10.42.24.206", 54345)
        self.buttonArray = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
                            self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8,
                            self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12,
                            self.pushButton_13, self.pushButton_14, self.pushButton_15, self.pushButton_16,
                            self.pushButton_17, self.pushButton_18, self.pushButton_19, self.pushButton_20,
                            self.pushButton_21, self.pushButton_22, self.pushButton_23]

    def on_receive(self, query):
        print("receiving", query)
        datapackages = json.loads(query)

        for button, datapackage in zip(self.buttonArray, datapackages):
            if datapackages[0]["votes"] <= 0:
                x=0
            else:
                x=datapackage["votes"]/datapackages[0]["votes"]
            r=(1-x)*255
            g=x*255
            rgb = str(r)+","+str(g)+",0"
            print(rgb)
            button.setStyleSheet("QPushButton { text-align: left; padding: 10px; background-color: rgb("+rgb+");}")
            self.wire_up_button(datapackage, button)

    def wire_up_button(self, datapackage, button):
        try:
            button.clicked.disconnect()
        except:
            Exception

        print("wireup")
        title, songid = datapackage["title"], datapackage["songid"]
        button.setText(title + " (" + str(datapackage["votes"]) + ")")
        button.clicked.connect(lambda: self.upvote(songid))


    def upvote(self, sid):
        text = '{"action":"upvote", "value":"' + sid + '"}\n'
        #if text!=self.lastvote:
        self.lastvote=text
        print(text)
        self.send(text)




class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VotingClient()
    sys.exit(app.exec_())
