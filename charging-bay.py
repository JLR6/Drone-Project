import time
from somelogging.library import Logger as Log
# logging is CRUCIAL
# I haven't included any actual logging in this pseudocode because its repetitive

# code to check whether the drone has been docked
def check_for_drone():
    return drone.status # a "drone" object containing basic information like
                        # location (i.e., is it docked or not), connectivity,
                        # etc. We can return False if we couldn't get the drone
                        # object (drone didn't dock)


def get_battery_status(drone):
    # this info will largely be collected from hardware APIs,
    # and will require collaboration w/ avionics team
    return # return a battery object containing a status field, which can be a
           # string from an enum (e.g. 'FULL') or a number denoting percentage


def get_sun_pos():
    return # use previous data to return the approximate location of the sun in the sky


def initiate_charging(battery):
    if battery.status == 'FULL':
        return
    while battery.status != 'FULL':
        # code to charge the battery by a certain increment goes here...
        charge(battery)
        status = get_battery_status()


# void method for battery swapping process
def swap_battery(drone):
    # code to swap battery goes here...
    initiate_charging(get_battery_status(drone))


def clean_solar_panels(drone):
    # void method to clean solar panels given drone object
    # should communicate with mechanical team for this part


def adjust_solar_panels(position):
    # adjust (move) the solar panels towards the given position (of the sun)
    # also might have to talk to mechanical team for this part


def unix_timestamp():
    return int(time.time())


def main():
    cleaning_interval = 3*60*60 # number of seconds in 3 hours
    sun_tracking_switch = True

    active = True
    while active:
        try:
            drone = check_for_drone()
            if drone:
                swap_battery(drone)
        except DroneError: # we can make custom error/exception definitions
            # handle & log errors (log to stdout or GUI)
            active = False

        if unix_timestamp() % cleaning_interval == 0:
            try:
                # I honestly forgot if Python variables are method-scoped or not,
                # but the final code could look something like this:
                clean_solar_panels(drone)
            except CleaningError:
                # handle & log errors
                active = False

            if sun_tracking_switch:
                try:
                    adjust_solar_panels(get_sun_pos())
                    sun_tracking_switch = not sun_tracking_switch
                except SolarError:
                    # the error-handling is very messy rn (so is the code),
                    # but it can be refined later
                    active = False


if __name__ == '__main__':
    main()
