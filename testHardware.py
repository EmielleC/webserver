import interface
 
class testhardware(interface.motorHardware) :
    def setup():
        print("setting up==========================================")
    def moveMotor(servo, radValue ):
        print("Moving motor")
 