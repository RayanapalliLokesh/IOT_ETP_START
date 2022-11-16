import RPi.GPIO as GPIO
import urllib2
import requests
import time
import json

from time import sleep
from rpi_lcd import LCD

sensor = 38
buzzer = 36

lcd = LCD()
red_pin = 11
orange_pin = 13
green_pin = 15

myAPI = 'RVLR5XXA9JI47ICZ'

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

PIN_TRIGGER = 7
PIN_ECHO = 16
	
T_TRIGGER = 29
T_ECHO = 31

GPIO.setup(T_TRIGGER, GPIO.OUT)
GPIO.setup(T_ECHO, GPIO.IN)
	
	
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
	
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(orange_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

GPIO.output(buzzer,False)
print "IR Sensor Ready....."
print " "

try: 
   while True:
     GPIO.output(PIN_TRIGGER, GPIO.LOW)
     GPIO.output(PIN_TRIGGER, GPIO.HIGH)
     time.sleep(0.00001)
     
     GPIO.output(PIN_TRIGGER, GPIO.LOW)
     while GPIO.input(PIN_ECHO) == 0:
       pulse_start_time = time.time()
     while GPIO.input(PIN_ECHO) == 1:
       pulse_end_time = time.time()
			
		pulse_duration = (pulse_end_time - pulse_start_time)
		distance = round(pulse_duration * 17150)
		
		print('Vehicle Distance = '+'%dcm'%distance)
    
    GPIO.output(T_TRIGGER, GPIO.LOW)
		GPIO.output(T_TRIGGER, GPIO.HIGH)
		
		time.sleep(0.00001)
		GPIO.output(T_TRIGGER, GPIO.LOW)
		
		while GPIO.input(T_ECHO) == 0:
			t_pulse_start_time = time.time()
		while GPIO.input(T_ECHO) == 1:
			t_pulse_end_time = time.time()
			
		t_pulse_duration = (t_pulse_end_time - t_pulse_start_time)
		t_distance = round(t_pulse_duration * 17150)
		
		print('Train Distance = '+'%dcm'%t_distance)
    
    if distance < 20 :
			if t_distance < 20:
				conn = urllib2.urlopen(baseURL + '&field1=%d' % (0))
				conn.close()
        
        if GPIO.input(sensor):
          GPIO.output(buzzer,False)
          
          while GPIO.input(sensor):
              time.sleep(1)
        else:
          GPIO.output(buzzer,True)
          print "Object Detected"
          time.sleep(1)
				
			else:
				conn = urllib2.urlopen(baseURL + '&field1=%d' % (1))
				conn.close()
					
		else:
			conn = urllib2.urlopen(baseURL + '&field1=%d' % (0))
			conn.close()
      if GPIO.input(sensor):
          GPIO.output(buzzer,False)
          
          while GPIO.input(sensor):
              time.sleep(0.5)
      else:
          GPIO.output(buzzer,True)
          print "Object Detected"
          time.sleep(1)	
		
		lcd.text("Punjab Police",1,2)
		sleep(1)
		
		lcd.clear()


except KeyboardInterrupt:
    GPIO.cleanup()
