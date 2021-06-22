import serial
import interface
import math 



class simpleServo(interface.motorHardware) :
    
    def __init__(self):
        self.ser =  serial.Serial(
        port = '/dev/ttyACM0',
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1
        )
        print("serial connection initialised" )
    
    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def setup():
        print("setting up")
    def moveMotor(self, servo, radValue ):
        #value = self.map((float(radValue)*-1), -1.0, 1.0, 0, 180)
        if (servo % 2) == 0:
            value = self.map((float(radValue)*-1), -1.0, 1.0, 60, 100)
        else:
            value = self.map((float(radValue)*-1), (math.pi / -2), (math.pi / 2), 30, 150)
        print(value)
        self.ser.write(('p %d %d\n' % (servo, value)).encode())
