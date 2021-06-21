import interface
import time

def current_milli_time():
    return round(time.time() * 1000)
 
class testHardware(interface.motorHardware) :
    
    def __init__(self):
        self.lastMeasure = current_milli_time()
        self.messagesReceived = 0
    def setup():
        print("setting up==========================================")
    def moveMotor(self, servo, radValue):
        self.messagesReceived = self.messagesReceived + 1
        if current_milli_time() >=  (self.lastMeasure + 1000):
            self.lastMeasure = current_milli_time()
            print(self.messagesReceived)
            self.messagesReceived  = 0
        #if servo == 1:
        #    print(radValue)
        #print("servo")
        #print(servo)
        #print("radValue")
        #print(radValue)
 