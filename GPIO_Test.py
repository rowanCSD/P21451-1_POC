import RPi.GPIO as GPIO ## Import GPIO library
import time

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(12, GPIO.OUT) ## Setup GPIO Pin 12 to OUT
GPIO.output(12,True) ## Turn on GPIO pin 12
wait(2)
GPIO.output(12,False)
