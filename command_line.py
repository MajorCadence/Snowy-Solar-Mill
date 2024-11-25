# Yuletide Twister Rev 1.002
# Made with love by Jennifer, Sara, and Connor
# William and Mary - SI Lab 2024 for Prof. Ran Yang

import RPi.GPIO as gpio # import the RPi.GPIO python library
from time import sleep # import the sleep function so we can sleep
import sys
import math
sys.path.insert(0, './Gamepad-Lib')
import Gamepad

is_debug = False # set to true to process debugging information
steps_per_rev = 200 # Adjusted for a NEMA17: the stepper has 200 steps per revolution

speedDirectionStick = 'LAS_Y_Axis'
exitButton = 'Home'
toggleControlButton = "L_Stick_Press"
speedAxis = 'DPAD_Y_Axis'
directionAxis = 'DPAD_X_Axis'
lightShow1Button = 'A'
lightShow2Button = 'X'
lightShow3Button = 'Y'
lightShow4Button = 'B'
lightShowToggleButton = 'RB'
musicToggleButton = 'LB'
musicTrackUpButton = 'Plus'
musicTrackDownButton = 'Minus'
microphoneEnableButton = 'LT'
microphoneDisableButton = 'RT'

pause_time = 0
RPM = 10
max_rpm_limit_step_mode = 100
max_rpm_limit_stick_mode = 25
clockwise = 0
new_direction = 0
rowQ = 0x1
rowR = 0x3
running = True
toggleMode = 0
light_show_enabled = True
light_show = 1
music_enabled = False
music_track = 1
microphone_enabled = False

# The code is for rotating with half steps
def main():
    
    print("Yuletide Twister Rev 1.0")
    print("Constructed by Sara, Jennifer, and Connor")
    reset_gpios()
    stepper()
                
                

def four_bit_rotation(direction, num1): # this code does a bit shift (bit rotation) in a particular direction for a 4-bit number
    
    if direction: # if the direction of the bit rotation is right (==1)
        return (2**4-1)&(num1>>1|num1<<(4-1)) 
            # shift the number to the right one bit, and also calculate the number left shifted three bits
            # OR the results together
            # (the ensures that the number is right-shifted one bit, but also that bit 0 becomes the new bit 3)
            # take only the lower four bits by ANDing with 0xF, ending up with an overall one bit rotation to the right
    
    else: # if the direction of the bit rotation is left (==0)
        return (2**4-1)&(num1<<1|num1>>(4-1))
            # shift the number to the left one bit, and also calculate the number right shifted three bits
            # OR the results together
            # (the ensures that the number is left-shifted one bit, but also that bit 3 becomes the new bit 0)
            # take only the lower four bits by ANDing with 0xF, ending up with an overall one bit rotation to the left

def calculate_motor_time_step_from_RPM(rpm):
    rps = int(rpm) / 60 # from the rpm (converted to int), calculate the rps (Rotations Per Second)
    steps_per_second = steps_per_rev * rps # using steps / rev, convert rev / s -> steps / s
    if steps_per_second == 0:
        seconds_per_step = 1
    else:
        seconds_per_step = 1 / steps_per_second # reciprocal to convert to seconds / step
    
    # since we rotate in half steps, we require the time interval (seconds / step) to be split evenly
    global pause_time 
    pause_time = seconds_per_step/2  # the pause time should be half of seconds / step ^^^^

def calculate_motor_RPM_from_timestep(timestep):
    seconds_per_step = pause_time * 2
    steps_per_second = 1 / seconds_per_step
    rps = steps_per_second / steps_per_rev
    global RPM
    RPM = rps * 60



def stepper(): # this is the main motor rotation function
    global rowQ, rowR, clockwise, new_direction
    calculate_motor_time_step_from_RPM(RPM)    
    while running and controller.isConnected():
        
        rowQ = four_bit_rotation(clockwise, rowQ) # bit rotate row-Q to get the next odd row (row-Q + 2)
        
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
        #debug_pause()

        sleep(pause_time) # pause for the calculated amount of time
        rowR = four_bit_rotation(clockwise, rowR) # bit rotate row-R to get the next even row (row-R + 2)
        
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
        #debug_pause()

        sleep(pause_time) # pause for the calculated amount of time

        #check if the direction has been switched

        

        if new_direction != clockwise:
            clockwise = new_direction
            temp = rowQ
            rowQ = rowR
            rowR = temp
    

def wait_for_connection(gamepadType):
    if not Gamepad.available():
        print("Please connect the controller to the windmill...")
        while not Gamepad.available():
            sleep(1)
    gamepad = gamepadType()
    print("Gamepad connected...")
    return gamepad

def setup_GPIOS():
    gpio.setmode(gpio.BCM) # use the broadcom board numbering
    ain1 = 26 # AOUT_1 = RED <- Ain1 asssigned to GPIO pin 26, Aout1 connection to motor has the red wire
    ain2 = 19 # AOUT_2 = YELLOW <- Ain2 asssigned to GPIO pin 19, Aout2 connection to motor has the yellow wire
    bin1 = 6  # BOUT_2 = GREEN <- Bin1 asssigned to GPIO pin 6, Bout1 connection to motor has the green wire
    bin2 = 13 # BOUT_1 = GREY <- Bin2 asssigned to GPIO pin 13, Bout2 connection to motor has the grey wire

    # set up Ain1, Ain2, Bin1, and Bin2 as GPIO outputs
    gpio.setup(ain1, gpio.OUT)
    gpio.setup(ain2, gpio.OUT)
    gpio.setup(bin1, gpio.OUT)
    gpio.setup(bin2, gpio.OUT)
    return ain1, ain2, bin1, bin2


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

def speedDirectionAxisMoved(new_position: int):
    global new_direction
    print(f"Speed control updated | New RPM {abs(new_position)*max_rpm_limit_stick_mode}")
    calculate_motor_time_step_from_RPM(abs(new_position)*max_rpm_limit_stick_mode)
    if new_position != 0:
        if new_position == abs(new_position):
            new_direction = 0
            print(f"Direction control updated | Rotation clockwise")
        else:
            new_direction = 1
            print(f"Direction control updated | Rotation counter-clockwise")

def exitButtonPressed():
    global running
    running = running ^ 1

def toggleControlButtonPressed():
    global toggleMode
    if not toggleMode:
        controller.removeAxisMovedHandler(speedAxis, speedAxisMoved)
        controller.removeAxisMovedHandler(directionAxis, directionAxisMoved)
        controller.addAxisMovedHandler(speedDirectionStick, speedDirectionAxisMoved)
        speedDirectionAxisMoved(0)
        print("Toggling control mode | Stick control")
    else:
        controller.removeAxisMovedHandler(speedDirectionStick, speedDirectionAxisMoved)
        controller.addAxisMovedHandler(speedAxis, speedAxisMoved)
        controller.addAxisMovedHandler(directionAxis, directionAxisMoved)
        print("Toggling control mode | D-PAD control")
        calculate_motor_time_step_from_RPM(0.5*max_rpm_limit_step_mode)
    toggleMode = toggleMode ^ 0b1

def speedAxisMoved(change: int):
    global pause_time
    if change < 0:
        pause_time /= 1.3
        calculate_motor_RPM_from_timestep(pause_time)
        if RPM > max_rpm_limit_step_mode:
            pause_time *= 1.3
            calculate_motor_RPM_from_timestep(pause_time)
        print(f"Speed inreased | New RPM {RPM}")
    elif change > 0:
        pause_time *= 1.3
        calculate_motor_RPM_from_timestep(pause_time)
        if RPM < 1: 
            pause_time /= 1.3
            calculate_motor_RPM_from_timestep(pause_time)
        print(f"Speed decreased | New RPM {RPM}")


def directionAxisMoved(change: int):
    global new_direction
    if change > 0:
        new_direction = 1
        print("Direction set to clockwise")
    elif change < 0:
        new_direction = 0
        print("Direction set to counter-clockwise")

def lightShow1Selected():
    global light_show
    light_show = 1
    print('Light show 1 selected')

def lightShow2Selected():
    global light_show
    print('Light show 2 selected')
    light_show = 2

def lightShow3Selected():
    global light_show
    print('Light show 3 selected')
    light_show = 3

def lightShow4Selected():
    global light_show
    print('Light show 4 selected')
    light_show = 4

def lightShowToggle():
    global light_show_enabled
    light_show_enabled = light_show_enabled ^ 1
    if light_show_enabled:
        controller.addButtonPressedHandler(lightShow1Button, lightShow1Selected)
        controller.addButtonPressedHandler(lightShow2Button, lightShow2Selected)
        controller.addButtonPressedHandler(lightShow3Button, lightShow3Selected)
        controller.addButtonPressedHandler(lightShow4Button, lightShow4Selected)
    else:
        controller.removeButtonPressedHandler(lightShow1Button, lightShow1Selected)
        controller.removeButtonPressedHandler(lightShow2Button, lightShow2Selected)
        controller.removeButtonPressedHandler(lightShow3Button, lightShow3Selected)
        controller.removeButtonPressedHandler(lightShow4Button, lightShow4Selected)
    print(f'Light show is enabled {light_show_enabled}')

def musicToggle():
    global music_enabled
    music_enabled = music_enabled ^ 1
    if music_enabled:
        controller.addButtonPressedHandler(musicTrackUpButton, musicTrackUp)
        controller.addButtonPressedHandler(musicTrackDownButton, musicTrackDown)
    else:
        controller.removeButtonPressedHandler(musicTrackUpButton, musicTrackUp)
        controller.removeButtonPressedHandler(musicTrackDownButton, musicTrackDown)
    print(f'Music is enabled {music_enabled}')

def musicTrackUp():
    global music_track
    music_track = ((music_track) % 8) + 1
    print(f"Music track up | Now playing track {music_track}")


def musicTrackDown():
    global music_track
    music_track = ((music_track - 2) % 8) + 1
    print(f"Music track down | Now playing track {music_track}")


def microphoneEnabled():
    global microphone_enabled
    microphone_enabled = True
    print(f"Microphone enabled {microphone_enabled}")

def microphoneDisabled():
    global microphone_enabled
    microphone_enabled = False
    print(f"Microphone enabled {microphone_enabled}")

if __name__ == "__main__": # are we running as a script ? This is the check that will execute our user code
    while running:
        try:
            ain1, ain2, bin1, bin2 = setup_GPIOS()
            controller = wait_for_connection(Gamepad.Custom_Nintendo)
            controller.startBackgroundUpdates()
            controller.addButtonPressedHandler(toggleControlButton, toggleControlButtonPressed)
            controller.addButtonPressedHandler(exitButton, exitButtonPressed)
            controller.addAxisMovedHandler(speedAxis, speedAxisMoved)
            controller.addAxisMovedHandler(directionAxis, directionAxisMoved)
            controller.addButtonPressedHandler(lightShow1Button, lightShow1Selected)
            controller.addButtonPressedHandler(lightShow2Button, lightShow2Selected)
            controller.addButtonPressedHandler(lightShow3Button, lightShow3Selected)
            controller.addButtonPressedHandler(lightShow4Button, lightShow4Selected)
            controller.addButtonPressedHandler(lightShowToggleButton, lightShowToggle)
            controller.addButtonPressedHandler(musicToggleButton, musicToggle)
            controller.addButtonPressedHandler(microphoneEnableButton, microphoneEnabled)
            controller.addButtonPressedHandler(microphoneDisableButton, microphoneDisabled)

            main()
            print("Power Off")
            reset_gpios()
            controller.removeAllEventHandlers()
            controller.addButtonPressedHandler(exitButton, exitButtonPressed)
            light_show_enabled = False # This is where we would ideally kill the light show thread and music threads
            music_enabled = False
            while not running:
                sleep(0.3)
            print("Power On")


        except OSError:
            print("Gamepad Error ? Please plug in gamepad")
        except IOError:
            print("Gamepad Error ? Please plug in gamepad")
        except KeyboardInterrupt: # if CTRL+C is pressed
            print("CTRL+C Pressed")
            running = False        
        finally:
            gpio.cleanup()  # make sure to cleanup the GPIO pins (reset them all to high-impendance inputs)
                            # when the program is finished
            controller.removeAllEventHandlers()
            controller.disconnect()
            light_show_enabled = False # This is where we would ideally kill the light show thread and music threads
            music_enabled = False

    print("Finished!")