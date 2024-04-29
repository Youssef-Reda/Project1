import serial
import time
import struct

k = struct.pack('B', 0xff)


def wbyte():
    ser.write(k)
    ser.write(k)
    ser.write(k)


ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)


# i = 0
# while(i < 101):
#     y = int(i)
#     y = str(y)
#     ser.write("j0.val=".encode())
#     ser.write(y.encode())
#     wbyte()
#     i = i+5
#     time.sleep(0.2)

while(True):
    data1 = str('"Rebooting.."')
    ser.write("t1.txt=".encode())
    ser.write(data1.encode())
    wbyte()
    time.sleep(3)
    data1 = str('" "')
    ser.write("t1.txt=".encode())
    ser.write(data1.encode())
    wbyte()
    time.sleep(3)
    ser.write("page 1".encode())
    wbyte()
    ioput = '0'
    while(ioput != '13'):
        resp = ser.read()
        resp = str(resp)
        print(resp)
        ioput = resp[-3:-1]
        print(ioput)

    ser.write("page 0".encode())
    wbyte()
    time.sleep(5)
