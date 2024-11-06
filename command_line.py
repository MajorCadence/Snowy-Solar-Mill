import RPi.GPIO as gpio
from time import sleep
gpio.setmode(gpio.BCM)
from scipy.optimize import curve_fit

ain1 = 26
ain2 = 19
bin1 = 6
bin2 = 13

steps_per_rev = 200

gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(bin1, gpio.OUT)
gpio.setup(bin2, gpio.OUT)

x=[1.5,2.17,2.86,3.54,4.21,4.89,5.57,6.25,6.93,7.61,8.29,8.96,9.64,10.32,11]
y=[0,10,25,40,52.5,65,75,90,105,117.5,132,147.5,160,170,180]

def linear_function(x,m,b):
    return m*x + b
    
popt, pcov = curve_fit(linear_function, x, y)
m, b = popt

servo = 5

gpio.setup(servo, gpio.OUT)

freq = 50
pwm = gpio.PWM(servo, freq)
pwm.start(1.5)

def main():
    
    # This is a basic CLI implementation
    while True:
        print("[1] Control Stepper Motor")
        print("[2] Control Servo Motor")
        print("[3] Quit")
        user_input = input("Please enter selection : ")
        if user_input == "1":
            steps = input("How many steps to move the motor : ")
            direction = input("Direction?")
            stepper(steps, direction)

        elif user_input == "2":
            angle = int(input("What angle to move the servo to : "))
            servo(angle)

        elif user_input == "3":
            break
        else:
            print("Invalid input, please enter a valid choice")
            
    pwm.stop()   
    gpio.cleanup()
    print("Finished!")


def toggle1(direction, num1):
    if direction:
        return (2**4-1)&(num1>>1|num1<<(4-1))
    else:
        return (2**4-1)&(num1<<1|num1>>(4-1))

def toggle2(direction, num2):
    if direction:
        return (2**4-1)&(num2>>1|num2<<(4-1))
    else:
        return (2**4-1)&(num2<<1|num2>>(4-1))

def stepper(steps, direction):

    counterclockwise=int(direction)

    if counterclockwise:
        num1 = 0x1
        num2 = 0x3
    else:
        num1 = 0x1
        num2 = 0x3  

    period = 0.01
    freq = 1/period
    rev_amount = 2
    degrees_per_step = 360/steps_per_rev
    total_steps = int(steps)

    for i in range(total_steps):
        try:
            num1 = toggle1(counterclockwise, num1)
            a1 = num1 >> 3 & 1
            b1 = num1 >> 2 & 1
            a2 = num1 >> 1 & 1
            b2 = num1 & 1
            gpio.output(ain1, a1)
            gpio.output(bin2, b1)
            gpio.output(ain2, a2)
            gpio.output(bin1, b2)

            #print(a1,b1,a2,b2)

            sleep(period)
        
            num2 = toggle2(counterclockwise, num2)
            a1 = num2 >> 3 & 1
            b1 = num2 >> 2 & 1
            a2 = num2 >> 1 & 1
            b2 = num2 & 1
            gpio.output(ain1, a1)
            gpio.output(bin2, b1)
            gpio.output(ain2, a2)
            gpio.output(bin1, b2)
        
        
            #print(a1,b1,a2,b2)

            sleep(period)
        
        
        except KeyboardInterrupt:
            break

def servo(angle):
    freq = 50
    period = 1/freq
    pwm.ChangeDutyCycle((angle - b)/m)
    sleep(1)


main()
