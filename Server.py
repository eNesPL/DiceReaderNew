import socket
import threading
from DiceReader import readDice
from time import sleep
from PiUi import Ui_MainWindow as ui


class Server:
    connected = False
    def Broadcast(self):
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ ip[ -1 ][ 0 ] for ip in interfaces ]
        while self.connected != True:
            for ip in allips:
                print(f'sending on {ip}')
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip, 0))
                sock.sendto("ILikeCake".encode(), ("255.255.255.255", 112))
                sock.close()
            sleep(2)

    def Connection_Tester(self,c):
        try:
            c.send("?".encode())
        except:
            self.connected=False
            threading.Thread(target=self.Broadcast).start()
            return False


    def Start(self):
        print("Server Started")
        s = socket.socket()
        port = 111
        s.bind(('', port))
        s.listen(1)
        print("is waiting")
        while(self.connected == False):
            c, addr = s.accept()
            self.connected=True
            print("connected")
            while True:
                if(self.Connection_Tester(c)==False):
                    break
                try:
                    data = c.recv(1024)
                    if data:
                        print(data)
                        if(data==b'GiveMeDice'):
                            print("SENDING")
                            try:
                                c.send((str(readDice()).encode()))
                            except:
                                c.send(b'0')
                        if(data==b'JustTestMe'):
                            self.Send_Command(c,"Music",99)
                except:
                    self.connected = False
                    threading.Thread(target=self.Broadcast).start()
                    break


    def Send_Command(self,c,cmd,val):
        c.send(str(cmd+":"+str(val)).encode())

