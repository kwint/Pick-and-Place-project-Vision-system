# Geschreven door Mitchel Mulder & Quinty van Dijk

import socket
import sys
import struct
from array import *

str1 = "\x1b[0;30;46m"
str2 = "\x1b[0m"

ip = '192.168.0.13'
port = 2000


# Function that sends data to PLC
def to_plc(x, y, block, color, degree, side):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_address = (ip, port)
    print(sys.stderr, str1 + 'connecting to %s port %s' % plc_address + str2)
    s.connect(plc_address)  # Hij wacht hier op de PLC

    while True:
        print(str1 + "Building array!" + str2)
        # 'h' gives 2 byte int value, do not use 'i' it wont work :((
        # [x,  y,  z, blok, kleur, draai, kant]
        arr = array('h', [x, y, block, color, degree, side])
        print(str1 + "Swapping array!" + str2, arr)
        # swap integer [BIG <> LITTLE endian]
        arr.byteswap()
        print(str1 + "Sending array:" + str2, arr)
        s.send(arr)
        print(str1 + "Bye!" + str2)
        s.close()


# Function that waits until plc has send ready signal
def from_plc():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    plc_address = (ip, port)
    print(sys.stderr, str1 + 'connecting to %s port %s' % plc_address + str2)

    s.connect(plc_address)  # Hij wacht hier op de PLC

    while True:
        try:
            a = s.recv(4906)  # Recieve from plc, Python stops here.
            break
        except Exception:
            print(str1 + "Can't connet to PLC! s.recv failure" + str2)

    b = struct.unpack(">h", a)[0]  # unpack the struct. place it in b position [0]
    print(str1 + "test 42" + str2)
    if b != 0:  # ">h" turn least and most significant bit
        print(str1 + "PLC is ready, start finding some blocks!" + str2)
        s.close()
        return
