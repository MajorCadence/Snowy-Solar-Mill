import RPi.GPIO as gpio # import the RPi.GPIO python library
from time import sleep # import the sleep function so we can sleep
gpio.setmode(gpio.BCM) # use the broadcom board numbering

ain1 = 26 # AOUT_1 = RED <- Ain1 asssigned to GPIO pin 26, Aout1 connection to motor has the red wire
ain2 = 19 # AOUT_2 = YELLOW <- Ain2 asssigned to GPIO pin 19, Aout2 connection to motor has the yellow wire
bin1 = 6  # BOUT_2 = GREEN <- Bin1 asssigned to GPIO pin 6, Bout1 connection to motor has the green wire
bin2 = 13 # BOUT_1 = GREY <- Bin2 asssigned to GPIO pin 13, Bout2 connection to motor has the grey wire

steps_per_rev = 200 # the motor has 200 steps per revolution

# set up Ain1, Ain2, Bin1, and Bin2 as GPIO outputs
gpio.setup(ain1, gpio.OUT)
gpio.setup(ain2, gpio.OUT)
gpio.setup(bin1, gpio.OUT)
gpio.setup(bin2, gpio.OUT)

# The code is for rotating with half steps

is_debug = False # set to true to process debugging information

def main():
    
    # This is a basic CLI implementation

    while True: # loop forever (until CTRL+C is pressed)
        try:
            reset_gpios() 
                            # reset all GPIOs to logic level low (0)
                            # to prevent excess current from flowing
                            # in the stepper motor when not rotating
                            # (don't lock the motor in place)

            print("[1] Control Stepper Motor")
            print("[2] Quit")
            user_input = input("Please enter selection : ") # process user input
            
            if user_input == "1": # if the user wants to move the stepper motor
                
                steps = input("How many steps to move the motor : ") # ask how many steps (full steps)
                direction = input("Direction?") # ask the direction (0=counterclockwise, 1=clockwise)
                rpm = input("RPM?") # ask the RPM of the motor (the speed)
                
                stepper(steps, direction, rpm) # run the motor rotation code with these parameters

            elif user_input == "2": # if the user wants to quit
                
                break # break out of the while loop
        
        except KeyboardInterrupt: # if CTRL+C is pressed
            
            break # break out of the while loop
    
    gpio.cleanup()  # make sure to cleanup the GPIO pins (reset them all to high-impendance inputs)
                    # when the program is finished
    
    print("Finished!")


def four_bit_rotation(direction, num1): # this code does a bit shift (bit rotation) in a particular direction for a 4-bit number
    
    if direction: # if the direction is right (==1)
        return (2**4-1)&(num1>>1|num1<<(4-1)) 
            # shift the number to the right one bit, and also calculate the number left shifted three bits
            # OR the results together
            # (the ensures that the number is right-shifted one bit, but also that bit 0 becomes the new bit 3)
            # take only the lower four bits by ANDing with 0xF, ending up with an overall one bit rotation to the right
    
    else: # if the direction is left (==0)
        return (2**4-1)&(num1<<1|num1>>(4-1))
            # shift the number to the left one bit, and also calculate the number right shifted three bits
            # OR the results together
            # (the ensures that the number is left-shifted one bit, but also that bit 3 becomes the new bit 0)
            # take only the lower four bits by ANDing with 0xF, ending up with an overall one bit rotation to the left

def stepper(steps, direction, rpm): # this is the main motor rotation function

    counterclockwise = int(direction) # convert string to int representing the direction

    if counterclockwise: # if the direction ends up being counterclockwise, start with the first two rows of the truth table
        rowQ = 0x3
        rowR = 0x1
        # 0 0 1 1
        # 0 0 0 1
    else:
        rowQ = 0x1
        rowR = 0x3
        # 0 0 0 1
        # 0 0 1 1
    
    rps = int(rpm) / 60 # from the rpm (converted to int), calculate the rps (Rotations Per Second)
    steps_per_second = steps_per_rev * rps # using steps / rev, convert rev / s -> steps / s
    seconds_per_step = 1 / steps_per_second # reciprocal to convert to seconds / step
    
    # since we rotate in half steps, we require the time interval (seconds / step) to be split evenly
    pause_time = seconds_per_step/2  # the pause time should be half of seconds / step ^^^^
    degrees_per_step = 360/steps_per_rev # convert steps / rev to degrees / step
    total_steps = int(steps) # total steps converted to integer (these are full steps)

    for i in range(total_steps): # loop for the total amount of steps
        try:
            rowQ = four_bit_rotation(counterclockwise, rowQ) # bit rotate row-Q to get the next odd row (row-Q + 2)
            
            a1 = rowQ >> 3 & 1  # grab bit 3 and assign it to a1
            b1 = rowQ >> 2 & 1  # grab bit 2 and assign it to b1
            a2 = rowQ >> 1 & 1  # grab bit 1 and assign it to a2
            b2 = rowQ & 1       # grab bit 0 and assign it to b2

            # write a1, b1, a2, b2 to the GPIO output pins
            gpio.output(ain1, a1)
            gpio.output(bin2, b1)
            gpio.output(ain2, a2)
            gpio.output(bin1, b2)

            # debugging print statements
            debug(("A1 A2 B2 B1"))
            debug((a1,a2,b2,b1))
            debug_pause()

            sleep(pause_time) # pause for the calculated amount of time
        
            rowR = four_bit_rotation(counterclockwise, rowR) # bit rotate row-R to get the next even row (row-R + 2)
            
            a1 = rowR >> 3 & 1  # grab bit 3 and assign it to a1
            b1 = rowR >> 2 & 1  # grab bit 2 and assign it to b1
            a2 = rowR >> 1 & 1  # grab bit 1 and assign it to a2
            b2 = rowR & 1       # grab bit 0 and assign it to b2
            
            # write a1, b1, a2, b2 to the GPIO output pins
            gpio.output(ain1, a1)
            gpio.output(bin2, b1)
            gpio.output(ain2, a2)
            gpio.output(bin1, b2)
        
            debug(("A1 A2 B2 B1")) # debugging print statements
            debug((a1,a2,b2,b1))
            debug_pause()

            sleep(pause_time) # pause for the calculated amount of time
        
        
        except KeyboardInterrupt: # if CTRL+C is pressed break out of the rotation loop (and back into the command-line loop)
            break



def debug(*message): # print debug messages if debug enabled
    if is_debug:
        for msg in message:
            print(msg)

def debug_pause(): # pause for user press key if debug enabled
    if is_debug:
        input()

def reset_gpios(): # write all zeros to the state of the current GPIO outputs
    gpio.output(ain1, 0)
    gpio.output(bin2, 0)
    gpio.output(ain2, 0)
    gpio.output(bin1, 0)

if __name__ == "__main__": # are we running as a script ? check that runs main() function
    main()
