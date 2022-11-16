import RPi.GPIO as GPIO
import time

sensor = 38
buzzer = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
print "IR Sensor Ready....."
print " "

try: 
   while True:
      if GPIO.input(sensor):
          GPIO.output(buzzer,False)
          
          while GPIO.input(sensor):
              time.sleep(1)
      else:
          GPIO.output(buzzer,True)
          print "Object Detected"
          time.sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()
