
"""  autonomously detect when a drone docks at the charging bay.
    initiate and control the battery swapping sequence once drone is detected.
    manage the battery charging process (starting, stopping, and monitoring charging status).
    detect when the solar panels need to be cleaned (either timed schedule or triggered event) and initiate the cleaning routine.
    adjust the orientation of the solar panels to track the sun.
    log major events and statuses for diagnostics.
    support basic remote monitoring via GUI. """
# credit: https://www.upesy.com/blogs/tutorials/hc-sr04-ultrasonic-sensor-on-rpi-pico-with-micropython-tutorial#
from machine import Pin, time_pulse_us
import time
import codey

SOUND_SPEED=340 
TRIG_PULSE_DURATION_US=10
#set up GPIO pins for ultrasonic sensor
trig_pin = Pin(15, Pin.OUT) #will depend on what pins are available on the board
echo_pin = Pin(14, Pin.IN)  

def manage_battery_swapping():
    print("Initiating battery swapping sequence.")
    # Logic to control the battery swapping mechanism
    # This could involve activating motors, relays, or other hardware components
    # to physically swap the battery.
    # For example:
    # motor_pin.value(1)  # Activate motor to move battery
    time.sleep(5)  # Simulate time taken for swapping
    print("Battery swapped successfully.")
def manage_battery_charging():
    print("Charging battery.")
    # monitoring battery status is difficult without a battery management system
    # either we need a chip that can monitor the battery status (https://learn.adafruit.com/adafruit-esp32-s2-tft-feather) 
    # or we can have to use some kind of voltage divider to measure the battery voltage
    # which will need more hardware and code to calculate the battery percentage
def clean_solar_panels():
    print("cleaning solar panels.")
    #requires a cleaning mechanism ex: brush with a servo
def adjust_solar_panels_orientation():
    #I've written solar tracking code before,
    #this is the link to the repo https://github.com/aryamantepal/Arduino-Solar-Tracker/blob/main/Arduino101.ino
    # we will have to change this to python and adapt it to the hardware we are using
    print("Adjusting solar panels orientation to track the sun.")
while True:
    trig_pin.value(0)
    time.sleep_us(5)
    trig_pin.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    trig_pin.value(0)

    ultrason_duration = time_pulse_us(echo_pin, 1, 30000)
    distance_cm = SOUND_SPEED * ultrason_duration / 20000

    print(f"Distance : {distance_cm} cm")
    time.sleep_ms(500)
    #depending on what we want to do add logic here to check distance and trigger actions
    if distance_cm < 20:  # Example threshold for docking detection
        print("Drone detected at docking station.")
        # Trigger battery swapping sequence here
        # manage_battery_swapping()
        # manage_battery_charging()
        # clean_solar_panels()
        # adjust_solar_panels_orientation()
        # log_event("Drone docked and battery swapping initiated.")
    else:
        print("No drone detected.")


