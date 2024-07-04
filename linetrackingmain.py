import RPi.GPIO as GPIO
from time import sleep

in1,in2,in3,in4,en,enb = 24,23,5,6,25,26
LeftSensor,CenterSensor,RightSensor = 4,14,15
#temp1=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([in1, in2, in3, in4, en, enb], GPIO.OUT)
GPIO.setup([LeftSensor, CenterSensor, RightSensor], GPIO.IN)

GPIO.output([in1, in2, in3, in4], GPIO.LOW)

p1=GPIO.PWM(in1,1000)
p2=GPIO.PWM(in2,1000)
p3=GPIO.PWM(in3,1000)
p4=GPIO.PWM(in4,1000)
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

changes = 0
allBlack = 0
twoBlack = 0

def move_forward():
    GPIO.output([in1,in3],GPIO.HIGH)
    GPIO.output([in2,in4],GPIO.LOW)

def turn_right():
    GPIO.output([in1,in2,in4],GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    
def turn_left():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output([in2,in3,in4],GPIO.LOW)
    
def stop():
    GPIO.output([in1,in2,in3,in4],GPIO.LOW)

def CallPrevious():
    global allBlack, twoBlack
    for i in range(0,4):
        if allBlack:
            print("Stopped while in CallPrevious")
            break
        if twoBlack:
            break
        if changes == 1:
            move_forward()
        elif changes == 2:
            turn_left()
        else:
            turn_right()
        print("Call Previous")
        
def sensorLoop():

    global allBlack,twoBlack,changes
    twoBlack = 0
    Left = GPIO.input(LeftSensor)
    Center = GPIO.input(CenterSensor)
    Right = GPIO.input(RightSensor)

		#[0,1,0]
    if Left==0 and Center==1 and Right==0: 
        move_forward()
        print("Moving Forward")
        p1.ChangeDutyCycle(80)
        p3.ChangeDutyCycle(80)
        p2.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)
        changes=1
		
    #[0,1,1]
    elif Left==0 and Center==1 and Right==1:
        turn_right()
        print("Right")
        p1.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)
        p4.ChangeDutyCycle(0)
        changes=3
        twoBlack = 1
        while True:
            turn_right()
            print("Hard right")
            if Left==0 and Center==1 and Right==0:
                break
            elif Left==1 and Center==0 and Right==0:
                break
            elif Left==1 and Center==1 and Right==1:
                break
		
    #[0,0,1]
    elif Left==0 and Center==0 and Right==1:
        turn_right()
        print("Right")
        p1.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)
        p4.ChangeDutyCycle(0)
        changes=3
        while True:
            turn_left()
            print("Slight Left")
            if Left==0 and Center==1 and Right==0:
                break
            elif Left==1 and Center==0 and Right==0:
                break
            elif Left==1 and Center==1 and Right==1:
                break

		#[1,1,0]
    elif Left==1 and Center==1 and Right==0:
        turn_left()
        print("Left")
        p1.ChangeDutyCycle(100)
        p3.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(100)
        changes=2
        twoBlack = 1
        while True:
            turn_left()
            print("Hard left")
            if Left==0 and Center==1 and Right==0:
                break
            elif Left==0 and Center==0 and Right==1:
                break
            elif Left==1 and Center==1 and Right==1:
                break

		#[1,0,0]
    elif Left==1 and Center==0 and Right==0:
        turn_left()
        print("Left")
        p1.ChangeDutyCycle(100)
        p3.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(100)
        changes=2
        while True:
            turn_right()
            print("Slight Right")
            if Left==0 and Center==1 and Right==0:
                break
            elif Left==0 and Center==0 and Right==1:
                break
            elif Left==1 and Center==1 and Right==1:
                break
   
   #[0,0,0]
    elif Left==0 and Center==0 and Right==0:
        print("No Track: Keeping Forward")
        p1.ChangeDutyCycle(70)
        p3.ChangeDutyCycle(70)
        p2.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)

		#[1,1,1]
    elif Left==1 and Center==1 and Right==1:
        allBlack = 1
        print("Detect Goal")

    else:
        pass
        
    if allBlack != 1 or twoBlack != 1:
        CallPrevious()
        
while True:
    if allBlack: 
    		break
    sensorLoop()

print("Ended")
GPIO.cleanup()

