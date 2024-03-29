import os
import socket
import threading

import psutil

from DiceReader import readDice
from time import sleep
import netifaces as ni



class Server:
    connected = False
    s=socket.socket()
    c=''


    def __init__(self,ui):
        self.ui = ui
    def Broadcast(self):
        allips = self.getips()
        while not self.connected:
            self.ui.stackedWidget.setCurrentIndex(0)
            print(self.connected)
            for ip in allips:
                try:
                    print(f'sending on {ip}')
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    sock.bind((ip, 0))
                    sock.sendto("ILikeCake".encode(), ("255.255.255.255", 2423))
                    sock.close()
                    sleep(1)
                except Exception as e:
                    print(e)

    def getIps_Handler(self):
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == socket.AF_INET:
                    yield snic.address
    def getips(self):
        ipv4s = list(self.getIps_Handler())
        return ipv4s

    def ConnectionTester(self, c):
        try:
            c.send("test".encode())
            print("just test")
        except:
            self.connected=False
            threading.Thread(target=self.Broadcast).start()
            return False

    def UpdateConnection(self, connection):
        self.c = connection

    def NewGame(self):
        self.SendCommand(self.c, "NewGame", 0)

    def Start(self):
        print("Server Started")
        s = socket.socket()
        port = 2422
        s.bind(('', port))
        s.listen(1)
        print("is waiting")
        print(self.connected)
        while(self.connected == False):
            print(self.connected)
            self.c, addr = s.accept()
            print(self.connected)
            self.connected=True
            self.ui.ChangeIndex(3)
            print("connected")
            self.UpdateConnection(self.c)
            while True:
                try:
                    data = self.c.recv(1024)
                    if data:
                        threading.Thread(target=self.HandleData(data)).start()
                except Exception as e:
                    print(e)
                    self.connected = False
                    threading.Thread(target=self.Broadcast).start()
                    break


    #def SendConfig(self):
     #   self.SendCommand(c, )

    def SendCommand(self, cmd, val):
        self.c.send(str(cmd+":"+str(val)).encode())

    def SendJson(self,json):
        print(json)
        self.c.send(str(json).encode())

    def HandleData(self,data):
        print(data)
        if (data == b'GiveMeDice'):
            print("SENDING")
            try:
                self.c.send((str(readDice()).encode()))
            except:
                self.c.send(b'0')
        if (data == b'SpawnOrMove'):
            self.ui.SpawnOrMove()
        else:
            if (data == b'TakeDice'):
                self.ui.TakeDiceConfirm()
            else:
                if (data == b'RollDiceMSG'):
                    self.ui.SetRollDice()
                else:
                    if ("MoveQuestion" in data.decode("utf-8")):
                        #print("I'tsheere")
                        self.ui.GenerateMoveButtons(data.decode("utf-8"))
                    else:
                        if (data == b"MovingPawn"):
                            self.ui.SetMovingPawn()