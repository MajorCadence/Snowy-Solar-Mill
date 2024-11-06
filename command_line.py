import RPi.GPIO as gpio
from time import sleep
gpio.setmode(gpio.BCM)

ain1 = 26 # AOUT_1 = RED
ain2 = 19 # AOUT_2 = YELLOW
bin1 = 6  # BOUT_2 = GREEN
bin2 = 13 # BOUT_1 = GREY

steps_per_rev = 200

gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(bin1, gpio.OUT)
gpio.setup(bin2, gpio.OUT)

#Half Steps

is_debug = False

def main():
    
    # This is a basic CLI implementation
    while True:
        try:
            print("[1] Control Stepper Motor")
            print("[2] Quit")
            user_input = input("Please enter selection : ")
            if user_input == "1":
                steps = input("How many steps to move the motor : ")
                direction = input("Direction?")
                rpm = input("RPM?")
                stepper(steps, direction, rpm)

            elif user_input == "2":
                break
        except KeyboardInterrupt:
            break      
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

def stepper(steps, direction, rpm):

    counterclockwise = int(direction)

    num1 = 0x1
    num2 = 0x3  

    period = 0.01
    freq = 1/period
    rev_amount = 2
    rps = int(rpm) / 60
    steps_per_second = 200 * rps
    seconds_per_step = 1 / steps_per_second
    pause_time = seconds_per_step/2
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

            debug((a1,b1,a2,b2))
            
            sleep(pause_time)
        
            num2 = toggle2(counterclockwise, num2)
            a1 = num2 >> 3 & 1
            b1 = num2 >> 2 & 1
            a2 = num2 >> 1 & 1
            b2 = num2 & 1
            gpio.output(ain1, a1)
            gpio.output(bin2, b1)
            gpio.output(ain2, a2)
            gpio.output(bin1, b2)
        
            
            debug((a1,b1,a2,b2))
            
            sleep(pause_time)
        
        
        except KeyboardInterrupt:
            break
def debug(*message):
    if is_debug:
        for msg in message:
            print(msg)

main()
