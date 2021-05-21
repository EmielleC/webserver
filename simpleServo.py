import serial
import interface


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class simpleServo(interface.motorHardware) :
    
    ser = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate = 115200,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    def setup():
        print("setting up==========================================")
    def moveMotor(servo, radValue ):
    
        value = _map((float(radValue)*-1), -1.00, 1.00, 0, 180)
        
        self.ser.write(('p %d %d\n' % (servo, value)).encode())

        print("Moving motor")