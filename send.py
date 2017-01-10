import socket
import sys
import struct
from array import *


def to_plc(x, y, z, blok, kleur, draai, kant):
    a = 1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_address = ('192.168.0.13', 2000)
    print(sys.stderr, 'connecting to %s port %s' % plc_address)
    s.connect(plc_address)  # Hij wacht hier op de PLC

    while True:
        b = 0
        print()
        print("Hi!")
        a = s.recv(4906)  # Recieve from plc, Python stops here.
        b = struct.unpack(">h", a)[0]  # unpack the struct. place it in b position [0]
        if b != 0:  # ">h" turn least and most significant bit
            print("Got something!")
            print("Building array!")
            ## 'h' gives 2 byte int value, do not use 'i' it wont work :((
            # [x,  y,  z, blok, kleur, draai, kant]
            arr = array('h', [0, 10, 103, 1034, 10345, 6000, 7000, 8000, 9000, 225])
            print("Swapping array!")
            ## swap integer [BIG <> LITTLE endian]
            arr.byteswap()
            print("Sending array!")
            s.send(arr)
            print("Bye!")
