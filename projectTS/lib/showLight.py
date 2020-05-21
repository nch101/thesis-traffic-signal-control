import RPi.GPIO as GPIO

class showLight():
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)

    def showLight(self, status):
        self.__turnoffAllLights()
        if (status == 'red'):
            GPIO.output(self.red_pin, GPIO.HIGH)
        elif (status == 'yellow'):
            GPIO.output(self.yellow_pin, GPIO.HIGH)
        elif (status == 'green'):
            GPIO.output(self.green_pin, GPIO.HIGH)
        else:
            pass

    def __turnoffAllLights():
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.yellow_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)