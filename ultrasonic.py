#Libraries
import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER = 23
GPIO_ECHO = 24
lcd = LCD() 

#mengubah arah GPIO (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def safe_exit(signum, frame):
    exit(1) 
def distance():
    # set nilai trigger 1 HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set nilai trigger setelah 0.00001 menjadi LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # menyimpan waktu kedatangan sinyal
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # perbedaan waktu antara start and arrival
    TimeElapsed = StopTime - StartTime
   #dikali dengan kecepatan suara 
    #dibagi dengan 2
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Jarak Terukur = %.2f cm" % dist)
            signal(SIGTERM, safe_exit)
            signal(SIGHUP, safe_exit)
            lcd.text("Jarak Terukur", 1)
            lcd.text("%.2f cm"%dist, 2)

            time.sleep(2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Pengukuran Diinterupsi oleh  User")
        GPIO.cleanup()
        pass
    finally:
        lcd.clear() 


