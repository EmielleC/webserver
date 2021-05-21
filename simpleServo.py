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
    
        rot2 = _map((float(arr[1])*-1), -1.00, 1.00, 0, 180)
        lin2 = _map((float(arr[2])*-1), -1.00, 1.00, 0, 180)
        rot1 = _map((float(arr[3])*-1), -1.00, 1.00, 0, 180)
        lin1 = _map((float(arr[4])*-1), -1.00, 1.00, 0, 180)
        
        ser.write(('p %d %d\n' % (servo, lin1)).encode())
        ser.write(('p %d %d\n' % (servo, rot1)).encode())
        ser.write(('p %d %d\n' % (servo, lin2)).encode())
        ser.write(('p %d %d\n' % (servo, rot2)).encode())
        
        print("Moving motor")