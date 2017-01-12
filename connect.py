import socket
import sys
import struct
from array import *

ip = '192.168.0.13'
port = 2000


# Function that sends data to PLC
def to_plc(x, y, block, color, degree, side):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_address = (ip, port)
    print(sys.stderr, 'connecting to %s port %s' % plc_address)
    s.connect(plc_address)  # Hij wacht hier op de PLC

    while True:
        print("Building array!")
        # 'h' gives 2 byte int value, do not use 'i' it wont work :((
        # [x,  y,  z, blok, kleur, draai, kant]
        arr = array('h', [x, y, block, color, degree, side])
        print("Swapping array!", arr)
        # swap integer [BIG <> LITTLE endian]
        arr.byteswap()
        print("Sending array:", arr)
        s.send(arr)
        print("Bye!")
        s.close()


# Function that waits until plc has send ready signal
def from_plc():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_address = (ip, port)
    print(sys.stderr, 'connecting to %s port %s' % plc_address)
    s.connect(plc_address)  # Hij wacht hier op de PLC
    while True:
        a = s.recv(4906)  # Recieve from plc, Python stops here.
        b = struct.unpack(">h", a)[0]  # unpack the struct. place it in b position [0]
        if b != 0:  # ">h" turn least and most significant bit
            print("PLC is ready, start finding some blocks!")
            s.close()
            return
