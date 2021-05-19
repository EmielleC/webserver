import serial
import interface

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
    
        #rot2 = _map((float(arr[1])*-1), -1.00, 1.00, 0, 180)
        #lin2 = _map((float(arr[2])*-1), -1.00, 1.00, 0, 180)
        #rot1 = _map((float(arr[3])*-1), -1.00, 1.00, 0, 180)
        #lin1 = _map((float(arr[4])*-1), -1.00, 1.00, 0, 180)
        
        #ser.write(('p %d %d\n' % ((int(0 + 2 * int(arr[0])), lin1))).encode())
        #ser.write(('p %d %d\n' % ((int(1 + 2 * int(arr[0])), rot1))).encode())
        #ser.write(('p %d %d\n' % ((int(4 + 2 * int(arr[0])), lin2))).encode())
        #ser.write(('p %d %d\n' % ((int(5 + 2 * int(arr[0])), rot2))).encode())
        
        print("Moving motor")