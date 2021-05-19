import abc

class motorHardware (abc.ABC):
    @abc.abstractmethod
    def setup():
        pass
    @abc.abstractmethod
    def moveMotor(servo, radValue ):
        pass