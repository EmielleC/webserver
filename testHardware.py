import interface
 
class testHardware(interface.motorHardware) :
    def setup():
        print("setting up==========================================")
    def moveMotor(servo, radValue ):
        if servo == 1:
            print(radValue)
        #print("servo")
        #print(servo)
        #print("radValue")
        #print(radValue)
 