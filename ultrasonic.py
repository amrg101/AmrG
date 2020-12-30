import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BOARD)

theft_buzzer = 11
stopTheftButton = 12
fire_buzzer = 13
stopFireButton = 15
trig = 16
echo = 18
dhtSensor = Adafruit_DHT.DHT11
dhtPin = 14
redLed = 31
greenLed = 29
theftExist = False
fireExist = False

def triggerUltraSonic():
    GPIO.output(trig, False)
    time.sleep(0.1)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

def measureDistance():
    while GPIO.input(echo)==0:
        pulseStart = time.time()
    while GPIO.input(echo)==1:
        pulseEnd = time.time()
    pulseDuration = pulseEnd - pulseStart
    distance = int(pulseDuration * 17150)
    return distance

def checkTemp():
    humidity , temperature = Adafruit_DHT.read_retry(dhtSensor, dhtPin)
    if temperature is not None:
        if temperature > 50:
            GPIO.output(fire_buzzer,1)
            fireExist = True

def check_ButtonStates():
    if (GPIO.input(stopTheftButton)==True):
        GPIO.output(theft_buzzer,0)
        theftExist = False
    if (GPIO.input(stopFireButton) == True):
        GPIO.output(fire_buzzer ,0)
        fireExist = False

def check_LedStates():
    if (theftExist == True and fireExist == True):
        GPIO.output(redLed , 1)
        GPIO.output(greenLed,0)
    elif(theftExist == False and fireExist == False):
        GPIO.output(redLed , 0)
        GPIO.output(greenLed,1)
    else:
        GPIO.output(redLed , 0)
        GPIO.output(greenLed,0)

def setupPins():
    GPIO.setup(trig,GPIO.OUT)
    GPIO.setup(echo,GPIO.IN)
    GPIO.setup(theft_buzzer,GPIO.OUT)
    GPIO.setup(stopTheftButton,GPIO.IN)
    GPIO.setup(fire_buzzer,GPIO.OUT)
    GPIO.setup(stopFireButton , GPIO.IN)
    GPIO.setup(redLed,GPIO.OUT)
    GPIO.setup(greenLed, GPIO.OUT)

setupPins()
while True:
    triggerUltraSonic()
    distance = measureDistance()
    if distance < 100:
        GPIO.output(theft_buzzer,1)
        theftExist = True
    checkTemp()
    currentTime = time.time()
    endTime = currentTime + 2
    while endTime < time.time():    # waits for 2 seconds and at the same time checks the states
        check_ButtonStates()        # this couldn't be done if we used time.sleep()
        check_LedStates()
GPIO.cleanup()	
