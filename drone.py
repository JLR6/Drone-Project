# micropython includes various libraries, but what is actually available 
# depends on the specific board and firmware version
# some libraries we might need/want: array, asyncio (async I/O scheduler), math,
# errno, io, os, select, time, ibus, toolkit
# micropy specific libraries: neopixel(if we want neopixels), micropython, machine (! very important !)


# to write portable code, just use the libraries available in micropython and not in port-specific libraries
# check docs

# might be helpful to reference this: https://github.com/TimHanewich/scout


#define pins, GPIO's, and other constants

#throttle settings

#alttitude settings (max rates of change)

#flight controller cycle time (times per second the flight controller updates, in hertz)


import machine
#import other libraries

#write the flight loop, everything in this kind of hardware programming is in a SINGLE loop
# this is the main loop that runs continuously
def flight_loop():
    print ("Starting flight loop")
    #some other code to indicate: the microcontroller is running, that the loop is running, etc.
    #maybe also show current time, throttle, altitude, etc.

    #set up RC receiver, or whatever input method we are using and check if successful
    print("RC receiver set up")

    #probably should use some sort of IMU
    #set up IMU and check if successful
    print("IMU set up")


    #set up motors PWM
    #set up anything else, calculate initial values, etc.

    #start the main loop
    #try: 
        #while True:
            #get start time
            #get IMU data
            #get RC input data
            #recalculate throttle and altitude based on input
            #set motor speeds based on throttle and altitude
             #do checks
        #exception handling



#OUTSIDE OF MAIN LOOP
#define helper functions, can also do this at the top of the file, but usually at the bottom to separate constants and functions
