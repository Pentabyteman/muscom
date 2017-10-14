#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import socket
import struct
import ssl
import pickle
from threading import Thread
import select
from PyQt5.QtCore import QObject


class SocketClient(QObject):
    def __init__(self):
        super(SocketClient, self).__init__()
        self.terminated = False
        self.connected = False
        self.log = " "
        print("Initialized socket client")

    def connect(self, host, port):
        print("print")
        try:
            print("Connecting to", host)
            self.socket = socket.socket()
            self.socket.connect((host, port))
            self.start()
            self.connected = True
            return True
        except socket.error:
            print("ERROR: Error while connecting!")
            self.connected = False
            return False

    def start(self):
        print("Client has started")
        Thread(target=self.handle_server).start()

    def disconnect(self):
        print("disconnecting")
        self.connected = False
        self.send("quit")
        self.terminated = True
        self.socket.close()

    def send(self, data):
        try:
            self.socket.sendall(data.encode("utf-8"))
        except Exception as e:
            print("ERROR: Error while sending", e)

    def handle_server(self):
        while not self.terminated:
            try:
                read_sockets, write_sockets, in_error = \
                    select.select([self.socket, ], [self.socket, ], [], 5)
            except select.error:
                print("FATAL ERROR: Connection error")
                self.socket.shutdown(2)
                self.socket.close()
            if len(read_sockets) > 0:
                index = self.log.find('\n')
                while index <= 0:
                    self.log += self.socket.recv(2048).decode()
                    index = self.log.find('\n')
                data = self.log[:index]
                self.log = self.log[index+1:]

                if len(data) > 0:
                        reply = self.data_received.emit(data)
                if len(write_sockets) > 0 and reply:
                    self.socket.send(reply.encode())
        print("finished handling server")

    def on_receive(self, query):
        pass

    def on_quit(self):
        pass

if __name__ == '__main__':
    client = SocketClient()
    client.connect("10.42.24.206", 54345)
