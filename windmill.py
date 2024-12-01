# Yuletide Twister Rev 1.013
# Made with love by Jennifer, Sara, and Connor
# William and Mary - SI Lab 2024 for Prof. Ran Yang

#TO-DO: add code to play music tracks asyncronously (possibly from beeper speaker over PWM pins?)
#       add code to cycle light shows asyncronously

import numpy as np # import numpy for processing
import RPi.GPIO as gpio # import the RPi.GPIO python library
import argparse # import argparse for pasring command line-arguments (partially set by this code)
from time import sleep # import the sleep function so we can sleep
import sys # import sys for importing additional libraries
import math # import for math functions
import threading # import for multithreading
from os import system # import system call for various uses
#import faulthandler # import for debugging segfaults
sys.path.insert(0, './Gamepad-Lib') # add the Piborg Gamepad library to the sys path
sys.path.insert(1, './project-keyword-spotter') # add the project-keyword-spotter to the sys path
import Gamepad # import the Piborg Gamepad library
import windmill_voice_recognition as KeywordModel # import the project-keyword-spotter library main call function


# the path to the text file of recognized keywords (the Coral Tensorflow model is designed to work only with these)
path_to_recognized_words = "./project-keyword-spotter/config/labels_gc2.raw.txt"

is_debug = False # set to true to process debugging information
steps_per_rev = 200 # Adjusted for a NEMA17: the stepper has 200 steps per revolution

# These variables define the button mapping for our controller

speedDirectionStick = 'LAS_Y_Axis' # The left analog stick movement to control the speed and direction in "stick" mode
exitButton = 'Home' # The home button will be the power button
toggleControlButton = 'L_Stick_Press' # The left stick press will toggle the control mode between "stick" and "D-PAD"
speedAxis = 'DPAD_Y_Axis'  # The D-PAD Y axis will (up-down) will control the speed in "D-PAD" mode
directionAxis = 'DPAD_X_Axis' # The D-PAD X axis (left-rigt) will control the rotation direction in "D-PAD" mode
lightShow1Button = 'A' # The A button will select light show #1
lightShow2Button = 'X' # The X button will select light show #2
lightShow3Button = 'Y' # The Y button will select light show #3
lightShow4Button = 'B' # The B button will select light show #4
lightShowToggleButton = 'RB' # The right bumper will toggle the light show on/off
musicToggleButton = 'LB' # The left bumper will toggle the music on/off
musicTrackUpButton = 'Plus' # The plus button will advance the music track
musicTrackDownButton = 'Minus' # The minus button will rewind to the previous music track
microphoneEnableButton = 'LT' # The left trigger will enable the microphone for voice control
microphoneDisableButton = 'RT' # The right trigger will disable (mute) the microphone

# These variables define the global values for our system, and are set to the following defaults

pause_time = 0 # The time interval between half setp rotations -> This is overwritten from the calculated RPM on start-up
RPM = 10 # The the default RPM to begin
max_rpm_limit_step_mode = 100 # The is the max RPM limit for the "D-PAD" control mode
max_rpm_limit_stick_mode = 25 # This is the max RPM limit for the "stick" control mode
clockwise = 0 # Begin with a counter-clockwise rotation [0=counter-clockwise, 1=clockwise]
new_direction = 0 # The new direction we should rotate (set to 0 for now)
rowQ = 0x1 # The very first row of the rotation truth table (0 0 0 1) in the form (a1, b1, a2, b2)
rowR = 0x3 # The next row at one half step later (0 0 1 1) in the form (a1, a2, b1, b2)
running = True # Whether or not the system is powered on (True)
toggleMode = 0 # The control mode we are currently in (0=DPAD mode, 1=Stick mode)
light_show_enabled = True # Start with the light show enabled
light_show = 1 # Start with the light show set to #1
music_enabled = False # Start with the music disabled
music_track = 1 # The music track will be set to the first track
microphone_enabled = False # Start with the microphone disabled
previous_keywords = ['', '', '', '', ''] # A buffer of previous detected keywords (default set to empty)


# The code is for rotating with half steps

def main(): # The main function which prints the build info and calls the stepper loop

    print("Yuletide Twister Rev 1.0")
    print("Constructed by Sara, Jennifer, and Connor")
    reset_gpios() # reset all GPIO outputs to low
    stepper() # call the main stepper loop
                
                

def four_bit_rotation(direction, num1): # this code does a bit shift (bit rotation) in a particular direction for a 4-bit number
# This bit rotation function is used to calculate the next stepping half step
    
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

def calculate_motor_time_step_from_RPM(rpm): # This function calculates the "pause_time" timestep between half steps from the current RPM value

    rps = int(rpm) / 60 # from the rpm (converted to int), calculate the rps (Rotations Per Second)
    steps_per_second = steps_per_rev * rps # using steps / rev, convert rev / s -> steps / s
    
    if steps_per_second == 0: # if we are not stepping at all (because RPM was set to zero, causing steps_per_second to be zero)
        # Then, we must set a non-infinite amount of time between each whole step, otherwise the stepper loop will sleep forever (and also we would end up dividing by zero here)
        seconds_per_step = 1 # I arbitrarily choose 1 second to be the "slowest" interval at lowest speed (an RPM of 0.3)
        
    else:
        seconds_per_step = 1 / steps_per_second # Otherwise, actually calculate it by taking the reciprocal to convert to seconds / step
        
    # now seconds_per_step is the time interval between every full step, but,
    # since we rotate in half steps, we require the time interval (seconds / step) to be split evenly between the half steps
    
    global pause_time # don't return it, but modify the global variable
    pause_time = seconds_per_step/2  # the pause time should be half of seconds / step ^^^^

def calculate_motor_RPM_from_timestep(timestep): # This function essentially does the reverse, calculating the RPM from the timestep (used later)

    seconds_per_step = pause_time * 2 # from the pause_time (the timestep of half steps), multiply by two to get seconds_per_step (the timestep of full steps)
    steps_per_second = 1 / seconds_per_step # take the reciprocal to find steps_per_second
    rps = steps_per_second / steps_per_rev # divide by steps / rev to calculate revolutions / sec
    
    global RPM # don't return it, but modify the global variable
    RPM = rps * 60 # multiply by 60 to arrive at the RPM


def stepper(): # this is the main motor rotation function, that loops

    global rowQ, rowR, clockwise, new_direction # Modify the global variables defined above
    calculate_motor_time_step_from_RPM(RPM) # calculate whatever the pause_time (half step timestep) should be based on the default RPM
    
    while running and controller.isConnected(): # Enter the main loop which should only break under CTRL+C, controller disconnect, or power button (running=False) pressed
        
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

        sleep(pause_time) # pause for the calculated amount of time (the half step timestep)
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

        sleep(pause_time) # pause for the calculated amount of time (the half step timestep)

        # check if the direction has been switched
        # if it has been, then we need to swap rowQ and rowR because
        # for the other direction we will be moving through the truth table backwards
        # and the half step row ordering must be reversed

        if new_direction != clockwise: # if the new_direction does not match the old direction, then the direction has changed
            clockwise = new_direction # quick algorithm to swap rowQ and rowR with a temporary variable
            temp = rowQ
            rowQ = rowR
            rowR = temp


def setup_Coral(): # this function initializes the Coral TPU accelerator and loads it with the keyword detection model's tensorflow file
    
    parser = argparse.ArgumentParser() # instantiate a new command line argument parser
    KeywordModel.add_model_flags(parser) # define arguments to look for and their default values
    
    # parse arguemnts; override the default path of the model file relative to the current directory
    args = parser.parse_args(['--model_file', './project-keyword-spotter/models/voice_commands_v0.7_edgetpu.tflite']) 
    interpreter = KeywordModel.make_interpreter(args.model_file) # initialize a new Coral interpreter
    interpreter.allocate_tensors() # allocte memory on the TPU for the tensors
    mic = args.mic if args.mic is None else int(args.mic) # possible override for the default microphone (not used; args.mic = None)

    return args, interpreter, mic # return the argument parser structure, and object of the interpreter, and the microphone ID number to use

def wait_for_connection(gamepadType): # this function waits for a controller to be connected and then returns a gamepad object that will be used to interface with the controller

    if not Gamepad.available(): # wait for a controller to be connected
        print("Please connect the controller to the windmill...")
        while not Gamepad.available(): # keep checking every second if a controller has been connected
            sleep(1)
    gamepad = gamepadType() # call the function addressed by the gamepad type that we pass in; this contains the keymapping info
    print("Gamepad connected...")
    return gamepad # return the gamepad object

def setup_GPIOS(): # this function sets up the GPIO pins as outputs with their correct pin numbering, then returns the pin numbering info

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


def debug(*messages): # print debug messages if debug enabled

    # This code prints all iterable messages in the container
    if is_debug:
        for msg in messages:
            print(msg)

def debug_pause(): # pause for user press key if debug enabled

    if is_debug:
        input()

def reset_gpios(): # write all zeros to the state of the current GPIO outputs, clearing them

    gpio.output(ain1, 0)
    gpio.output(bin2, 0)
    gpio.output(ain2, 0)
    gpio.output(bin1, 0)

def soft_power_off(): # called by the keyword parser for device power off

    global running # Use the global variable
    running = False # set the boolean determining power state to False

def soft_power_on(): # called by the keyword parser for device power on

    global running # Use the global variable
    running = True # set the boolean determining power state to False

def mute(): #called by the keyword parser for disabling the music

    global music_enabled # Use the global variable
    music_enabled = True # set the boolean determining music to be True
    musicToggle() # Then, enter the callback which will toggle it to False

def unmute(): #called by the keyword parser for enabling the music

    global music_enabled # Use the global variable
    music_enabled = False # set the boolean determining music to be False
    musicToggle() # Then, enter the callback which will toggle it to True

def lights_on(): # called by the keyword parser for enabling the light shows

    global light_show_enabled # Use the global variable
    light_show_enabled = False # set the boolean determining light show enable to be False
    lightShowToggle() # Then, enter the callback which will toggle it to True

def lights_off(): # called by the keyword parser for disabling the light shows

    global light_show_enabled # Use the global variable
    light_show_enabled = True # set the boolean determining light show enable to be True
    lightShowToggle() # Then, enter the callback which will toggle it to False

def exitButtonPressed(): # The callback function for the exit button press

    global running # Use the global variable
    running = running ^ 1 # toggle the boolean for running using XOR

def speedDirectionAxisMoved(new_position: int): # The callback function for the speed/direction stick moving

    global new_direction # Use the global variable
    if toggleMode: # Sanity check that the current control mode is stick control
        print(f"Speed control updated | New RPM {abs(new_position)*max_rpm_limit_stick_mode}")
        calculate_motor_time_step_from_RPM(abs(new_position)*max_rpm_limit_stick_mode) # Calculate the new time step from the RPM limit multiplied by the absolute value of stick position (ranging from 0 to 1)
        
        if new_position != 0: # If the stick is not in the center position
        
            if new_position == abs(new_position): # If the stick position is positive, then our direction is counter-clockwise
            
                new_direction = 0 # update the global new_direction variable
                print(f"Direction control updated | Rotation clockwise")
                
            else: # otherwise, the stick position must be negative
            
                new_direction = 1 # set the new_direction to be clockwise
                print(f"Direction control updated | Rotation counter-clockwise")


def toggleControlButtonPressed(): # The callback function for the control mode toggle switch

    global toggleMode # Use the global variable

    toggleMode = toggleMode ^ 0b1 # toggle the control mode boolean 'toggleMode' using XOR
    if toggleMode: # If the toggle_mode is now 1 (i.e. stick control), remove all handlers for the D-PAD control, and add the handler for stick control
    
        controller.removeAxisMovedHandler(speedAxis, speedAxisMoved)
        controller.removeAxisMovedHandler(directionAxis, directionAxisMoved)
        controller.addAxisMovedHandler(speedDirectionStick, speedDirectionAxisMoved)
        
        speedDirectionAxisMoved(0) # reset the speed to zero by directly calling the callback for stick control passing in a value for a centered stick
        print("Toggling control mode | Stick control")
        
    else: # Otherwise, if the toggle_mode is now 0 (i.e. D-PAD control), remove the handler for stick control, and add the handlers for D-PAD control
    
        controller.removeAxisMovedHandler(speedDirectionStick, speedDirectionAxisMoved)
        controller.addAxisMovedHandler(speedAxis, speedAxisMoved)
        controller.addAxisMovedHandler(directionAxis, directionAxisMoved)
        
        calculate_motor_time_step_from_RPM(0.5*max_rpm_limit_step_mode) # reset the speed by directly calculating a new timestep from an RPM of half the maximum for step mode
        print("Toggling control mode | D-PAD control")
        

def speedAxisMoved(change: int): # The callback function for the speed axis (D-PAD mode)

    global pause_time # Use the global variable
    if not toggleMode: # sanity check that the current control mode is D-PAD control
        if change < 0: # If the value is negative (D-PAD up)
        
            pause_time /= 1.3 # divide the current pause_time (increase speed) by 1.3 (arbitrary value)
            calculate_motor_RPM_from_timestep(pause_time) # calculate (and set) the new motor RPM from this new timestep
            
            if RPM > max_rpm_limit_step_mode: # if the RPM is now above our maximum limits
                pause_time *= 1.3 # then revert it
                calculate_motor_RPM_from_timestep(pause_time) # and calculate the old RPM
                
            print(f"Speed inreased | New RPM {RPM}")
            
        elif change > 0: # Otherwise, if the value is positive (D-PAD down)
        
            pause_time *= 1.3 # multiply the current pause_time (decrease speed) by 1.3 (arbitrary value)
            calculate_motor_RPM_from_timestep(pause_time) # calculate (and set) the new motor RPM from this new timestep
            
            if RPM < 1: # if the RPM is now below that previously imposed maximum pause_time value of 1 (at "0" RPM)
                pause_time /= 1.3 # then revert it; we don't want it too slow or the program will feel sluggish to respond
                calculate_motor_RPM_from_timestep(pause_time) # and calculate the old RPM
                
            print(f"Speed decreased | New RPM {RPM}")


def directionAxisMoved(change: int): # The callback function for the speed axis (D-PAD mode)

    global new_direction # Use the global variable
    if not toggleMode: # sanity check that the current control mode is D-PAD control
        if change > 0: # If the value is positive (D-PAD) right
        
            new_direction = 1 # rotate clockwise
            print("Direction set to clockwise")
            
        elif change < 0: # Otherwise, if the value is negative (D-PAD) left
        
            new_direction = 0 # rotate counter-clockwise
            print("Direction set to counter-clockwise")

def lightShow1Selected(): # The callback function for selecting light show #1
    
    global light_show # Use the global variable
    if light_show_enabled: # sanity check that the light show is actually enabled
        print('Light show 1 selected')
        light_show = 1 # set the light show number to 1

def lightShow2Selected(): # The callback function for selecting light show #2

    global light_show # Use the global variable
    if light_show_enabled: # sanity check that the light show is actually enabled
        print('Light show 2 selected')
        light_show = 2 # set the light show number to 2

def lightShow3Selected(): # The callback function for selecting light show #3

    global light_show # Use the global variable
    if light_show_enabled: # sanity check that the light show is actually enabled
        print('Light show 3 selected')
        light_show = 3 # set the light show number to 3

def lightShow4Selected(): # The callback function for selecting light show #4

    global light_show # Use the global variable
    if light_show_enabled: # sanity check that the light show is actually enabled
        print('Light show 4 selected')
        light_show = 4 # set the light show number to 4

def lightShowToggle(): # The callback function for enabling/disabling the light show

    global light_show_enabled # Use the global variable
    light_show_enabled = light_show_enabled ^ 1 # Toggle the boolean for the light show enable using XOR
    
    if light_show_enabled: # If the light show is now enabled, add the callback handlers for changing the current show number
    
        controller.addButtonPressedHandler(lightShow1Button, lightShow1Selected)
        controller.addButtonPressedHandler(lightShow2Button, lightShow2Selected)
        controller.addButtonPressedHandler(lightShow3Button, lightShow3Selected)
        controller.addButtonPressedHandler(lightShow4Button, lightShow4Selected)
        
    else: # If the light show is now disabled, remove the callback handlers for changing the current show number
    
        controller.removeButtonPressedHandler(lightShow1Button, lightShow1Selected)
        controller.removeButtonPressedHandler(lightShow2Button, lightShow2Selected)
        controller.removeButtonPressedHandler(lightShow3Button, lightShow3Selected)
        controller.removeButtonPressedHandler(lightShow4Button, lightShow4Selected)
        
    print(f'Light show is enabled {light_show_enabled}')

def musicToggle(): # The callback function for toggling the music

    global music_enabled # Use the global variable
    music_enabled = music_enabled ^ 1 # Toggle the boolean for the music enable using XOR
    
    if music_enabled: # If the music is now enabled, add the callback handlers for changing the music track
    
        controller.addButtonPressedHandler(musicTrackUpButton, musicTrackUp)
        controller.addButtonPressedHandler(musicTrackDownButton, musicTrackDown)
        
    else: # If the music is now disabled, remove the callback handlers for changing the music track
    
        controller.removeButtonPressedHandler(musicTrackUpButton, musicTrackUp)
        controller.removeButtonPressedHandler(musicTrackDownButton, musicTrackDown)
        
    print(f'Music is enabled {music_enabled}')

def musicTrackUp(): # The callback function for incrementing the music track

    global music_track # Use the global variable
    if music_enabled: # sanity check that the music is actually enabled
        music_track = ((music_track) % 8) + 1 # If music track goes outside the bounds of 1-8, mod 8 and add 1 to fix
        print(f"Music track up | Now playing track {music_track}")


def musicTrackDown(): # The callback function for incrementing the music track

    global music_track # Use the global variable
    if music_enabled: # sanity check that the music is actually enabled
        music_track = ((music_track - 2) % 8) + 1 # If music track goes outside the bounds of 1-8, subtract 2, mod 8 and add 1 to fix
        print(f"Music track down | Now playing track {music_track}")


def microphoneEnabled(): # The callback function for enabling voice control

    global microphone_enabled # Use the global variable
    
    microphone_enabled = True # Set to true
    print(f"Microphone enabled {microphone_enabled}")
    if not KeywordThread.is_alive(): # if the thread handling keyword processing is not started...
        KeywordThread.start() # ...start it asyncronously
    

def microphoneDisabled(): # The callback function for disabling voice control

    global microphone_enabled, KeywordThread # Use the global variable
    
    microphone_enabled = False # Set to false
    print(f"Microphone enabled {microphone_enabled}")
    if KeywordThread.is_alive(): # if the thread handling keyword processing is running...
        KeywordThread.join() # terminate it by waiting for it to exit, now that 'microphone_enabled' is false
        del KeywordThread # dealloc it and destroy the original object
        KeywordThread = createKeywordThread() # create a new instance of the thread with the same parameters
    
def createKeywordThread(): # this function creates and returns a thread object with the same parameters (to run the keyword listening model)
    
    # return a thread with:
        # the function target being run_model, a function in the loaded KeywordModel python file
        # passing arguments of the Coral TPU interpreter object, the path to the recognized word list
        # passing keyword arguments of the callback function for an individual Keyword parse operation
        # the number of frames of audio to process at a time (default 33)
        # the recorder context manager object (a pyaudio instance)
        # the break condition to exit its main while loop
            # this condition is a lambda function that will be called on every loop
            # it always will return the value of 'microphone_enabled' from this code file
    return threading.Thread(target = KeywordModel.run_model, 
                            args=(interpreter, path_to_recognized_words), 
                            kwargs=({'result_callback': evaluate_results,
                            'num_frames_hop': int(args.num_frames_hop),
                            'recorder': audio_recorder,
                            'break_condition': lambda : microphone_enabled}))

    # see windmill_voice_recognition.py for more info

def evaluate_results(result, commands, labels, top=3): # this is the callback function that parses the current detected audio
    """Example callback function that prints the passed detections."""
    
    # this code was copied entirely from the example file
    # only my code additions are commented, the rest remains to complicaed to explain here
    
    previous_keywords.pop() # pop the last item off of the previous keywords buffer

    top_results = np.argsort(-result)[:top]
    for p in range(top):
        l = labels[top_results[p]]
        if l in commands.keys():
         threshold = commands[labels[top_results[p]]]["conf"]
        else:
         threshold = 0.5
        if top_results[p] and result[top_results[p]] > threshold: # << This is the code that gets hit if we have a confident detection
         debug("\033[1m\033[93m*%15s*\033[0m (%.3f)" %
                        (l, result[top_results[p]]))
         
         
         perform_action_from_keyword(l) # Call my own function to perform an action based on the keyword detection, where 'l' is the keyword string
         
        elif result[top_results[p]] > 0.005:
         debug(" %15s (%.3f)" % (l, result[top_results[p]]))

    if len(previous_keywords) < 5: # if the previous keywords buffer is less than 5...
        previous_keywords.insert(0, '') # insert an empty string to the beginning
    debug(previous_keywords)

def perform_action_from_keyword(keyword): # this function takes in a detected keyword as a string and determines what action to perform
    
    global previous_keywords # use the global variable
    
    if keyword in previous_keywords: # if the keywords already exists in the previous keywords list...
        return # then return immediatly; do not perform an action, as the keyword might be a double or triple detection
    else:
        previous_keywords.insert(0, keyword) # otherwise, add this keyword into the previous keyword buffer
        
        if running == False: # now, check if the windmill has been soft powered off
            if keyword == 'switch_on': # if so, we should ignore all keywords except 'switch_on'
                soft_power_on() # if detected, call the power on function
            return # return now so we don't process other keywords
        

        # This is a dictionary mapping valid detecable keyword strings with a specific tuple
        # This tuple contains a function object that is callable, and an arguemnt to pass into that function
        action_mapping_args =   {
                                'turn_up': (speedAxisMoved, -1), 'turn_down': (speedAxisMoved, 1),
                                'turn_left': (directionAxisMoved, -1), 'turn_right': (directionAxisMoved, 1),
                                'reverse': (directionAxisMoved, -1 if clockwise else 1)
                                }
        
        # This is another dictionary mapping valid detecable keyword strings with a callable function object
        # This time, the called function needs no arguments
        action_mapping_no_args= {
                                'switch_off': soft_power_off, 'switch_on': soft_power_on,
                                'next_song': musicTrackUp, 'previous_song': musicTrackDown,
                                'channel_one': lightShow1Selected, 'channel_two': lightShow2Selected,
                                'channel_three': lightShow3Selected, 'channel_four': lightShow4Selected,
                                'mute': mute, 'unmute': unmute, 'start_video': lights_on, 'stop_video': lights_off,
                                'engage': toggleControlButtonPressed
                                }
        
        try: # wrap in a try block in case the detected keyword is not one we are interested in
            action_mapping_args.get(keyword)[0](action_mapping_args.get(keyword)[1]) # search the dictionary for the tuple corresponding to the keyword, call the function object from it, passing in the specific argument
            return # once we've executed the function object, return
        except TypeError: # it wasn't found in the first dictionary
            pass # continue on
        try:
            action_mapping_no_args.get(keyword)() # search the second dictionary with the keyword for the mapped callable function object, then call it
            return # once we've executed the function object, return
        except TypeError: # it wasn't found in either dictionary, it must have been a keyword we are not looking for
            debug("Keyword detected but not recognized as a valid action")

if __name__ == "__main__": # are we running as a script ? This is the check that will execute our user code

    while running: # Repeat while the exit signal is not given
        try:
            print("Setting up GPIOs...")
            # Start by setting up the GPIOs
            ain1, ain2, bin1, bin2 = setup_GPIOS() 

            print("Loading PyCoral model and parsing arguments...")
            # next, initialize the Coral TPU with the keyword model, and parse default arguments
            args, interpreter, mic = setup_Coral()
            
            print("Setting up PyAudio recording interface...")
            # start pyaudio audio recorder instance; this returns a custom context manager 
            #defined a code file in the Coral library (BUG DETECTED, see note at bottom)
            audio_recorder = KeywordModel.start_audio_recorder(mic, sample_rate_hz=int(args.sample_rate_hz)) 
            
            print("Threading online. Creating keyword detector async thread...")
            # create and return a new threading.thread object to be our asynchronous keyword detection function
            # parameters of which are defined in the function itself
            KeywordThread = createKeywordThread()

            print("Detecting game controller...")
            # Wait for a game controller to be connected, and give it our custom Nintendo mapping
            controller = wait_for_connection(Gamepad.Custom_Nintendo)

            print("Creating controller update thread and setting up callback functions...")
            controller.startBackgroundUpdates() # start the background update threads for the callbacks
            controller.addButtonPressedHandler(toggleControlButton, toggleControlButtonPressed) # Add the handler for toggling control mode
            controller.addButtonPressedHandler(exitButton, exitButtonPressed) # Add the handler for power on/off
            if toggleMode: # If we have defined the windmill to start in stick control mode...
                controller.addAxisMovedHandler(speedDirectionStick, speedDirectionAxisMoved) # add the handler for stick control of speed and direction
            else: # otherwise, it's defined to be in D-PAD control mode
                controller.addAxisMovedHandler(speedAxis, speedAxisMoved) # Add the handler for D-PAD control of speed
                controller.addAxisMovedHandler(directionAxis, directionAxisMoved) # Add the handler for D-PAD control of rotation direction
            if light_show_enabled: # if we have defined the windmill to start with the light show enabled...
                controller.addButtonPressedHandler(lightShow1Button, lightShow1Selected) # Add the handler for selecting light show 1
                controller.addButtonPressedHandler(lightShow2Button, lightShow2Selected) # Add the handler for selecting light show 2
                controller.addButtonPressedHandler(lightShow3Button, lightShow3Selected) # Add the handler for selecting light show 3
                controller.addButtonPressedHandler(lightShow4Button, lightShow4Selected) # Add the handler for selecting light show 4
            controller.addButtonPressedHandler(lightShowToggleButton, lightShowToggle) # Add the handler for enabling/disabling the light show
            if music_enabled: # if we have defined the windmill to start with the music playing function enabled...
                controller.addButtonPressedHandler(musicTrackUpButton, musicTrackUp)
                controller.addButtonPressedHandler(musicTrackDownButton, musicTrackDown)
            controller.addButtonPressedHandler(musicToggleButton, musicToggle) # Add the handler for enabling music (which will furthur enable the handlers for selecting different tracks)
            controller.addButtonPressedHandler(microphoneEnableButton, microphoneEnabled) # Add the handler for enabling microphone
            controller.addButtonPressedHandler(microphoneDisableButton, microphoneDisabled) # Add the handler for disabling microphone
            
            system('clear')
            main() # start the main function code
            
            print("Power Off") # once main quits, we know we got an exit signal from the power off button
            reset_gpios() # set all GPIOs to low
            controller.removeAllEventHandlers() # remove all event handlers
            controller.addButtonPressedHandler(exitButton, exitButtonPressed) #re-add the power button event handler so that we can turn the windmill back on with the controller if we want to
            # also, since the callbacks for keyword recognition are not part of the removed controller callbacks, we are still listening for keywords, such as switch_on
            
            light_show_enabled_temp = light_show_enabled # stash the current statuses of lights and music in temporary variables
            music_enabled_temp = music_enabled
            light_show_enabled = False # Stop the lights and music
            music_enabled = False
            
            while not running: # keep checking if "running" ever gets set to true; this means power back on
                sleep(0.3)
            print("Power On")
            
            # retore the statuses of the lights and music to what they were from the temporary variables
            music_enabled = music_enabled_temp
            light_show_enabled = light_show_enabled_temp

        except OSError: # catch gamepad errors if disconnected
            print("Gamepad Error ? Please plug in gamepad")
        except IOError: # catch gamepad errors if disconnected
            print("Gamepad Error ? Please plug in gamepad")
        except KeyboardInterrupt: # if CTRL+C is pressed
            print("CTRL+C Pressed")
            running = False # setting running to false at this point means that the entire script will exit; we want to completely exit on CTRL+C
            light_show_enabled = False # This is where we would ideally kill the light show thread and music threads
            music_enabled = False
        finally:
            gpio.cleanup()  # make sure to cleanup the GPIO pins (reset them all to high-impendance inputs)
                            # when the program is finished
            controller.removeAllEventHandlers() # remove all event handlers
            controller.disconnect() # terminate the background callback updater thread
            

    print("Finished!")