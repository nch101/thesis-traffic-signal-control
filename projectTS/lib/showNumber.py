import RPi.GPIO as GPIO
import time 

class showNumber:
    """
        Show number on LED 7 segment using HC595
    """
    def __init__(self, data_pin, clock_pin, latch_pin):
        """
            :param data_pin: Number. Pin to transmit bin code
            :param clock_pin: Number. Create clock
            :param latch_pin: Number. Permit show
        """
        self.data_pin = data_pin
        self.clock_pin = clock_pin
        self.latch_pin = latch_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
    
    def showNumber(self, number):
        if ((number > 99) or (number < 0)):
            raise ValueError('number needs to be between 0 - 99')
        self.__convertToBinLED(number)

    def __convertToBinLED(self, number):
        binLED = [
            '11000000',
            '11111001', 
            '10100100',
            '10110000', 
            '10011001',
            '10010010',
            '10000010',
            '11111000',
            '10000000',
            '10010000']

        unit = number % 10
        tens = int((number - unit) / 10)

        self.__transmit(binLED[unit])
        self.__transmit(binLED[tens])

    def __transmit(self, numLED):
        GPIO.output(self.latch_pin, GPIO.LOW)

        for i in range(0, 8):
            GPIO.output(self.clock_pin, GPIO.LOW)
            GPIO.output(self.data_pin, int(numLED[i]))
            GPIO.output(self.clock_pin, GPIO.HIGH)
        
        GPIO.output(self.latch_pin, GPIO.HIGH)
        
        
#
# Debug showNumber
#
#

# data_pin = 15
# clock_pin = 13
# latch_pin = 11
# test = showNumber(data_pin, clock_pin, latch_pin)
# 
# def main():
#     for i in range(0, 100):
#         test.showNumber(i)
#         time.sleep(1)
#     GPIO.cleanup()
# 
# 
# main()
