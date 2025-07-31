"""
- add more details to raised exceptions / error logging 
- add tests
- maybe a way to reset the arm to safe position if it gets stuck ? would need a reset if currently holding battery vs empty
- manual overrides?? ->  manual arm control ? manual trigger for solar panel cleaning ? manual control over solar panel angle ? etc

must run in parallel:
- charging, tracking, detection, cleaning all need to happen at same time
- some things run constantly (battery, drone detection), others can be timed (sun tracking, cleaning)
- blocking one task delays or breaks others

use threads or async to separate charging monitor, sun tracker, drone detector, etc
if no real parallelism, main loop must check fast enough to simulate it
"""

import time

class ChargingBay:
    """
    Main charging bay controller for Mars drone station
    """
    def __init__(self):
        self.system_start_time = time.time()
        self.drone_docked = False
        self.last_cleaning_time = time.time()
        self.cleaning_interval = 3 * 3600                   # idk set to 3 hours
        self.sun_position = 0
        self.arm_position = "home"
        self.charging_batteries = {}
        self.drone_arrival_time = None
        self.drone_departure_time = None
        self.last_swap_time = None
        self.current_drone_battery = None                   # battery id of battery currently in drone
        self.charging_bay_batteries = {                     # battery IDs of batteries in charging bay
            "slot_1": None,
            "slot_2": None
        }
        self.swap_status = "idle"                           # idle, in_progress, error, complete

    # DRONE DETECTION / DOCKING
    def detect_drone(self):
        """
        check if drone is at charging bay
        """
        drone_detected = True
        
        if drone_detected and not self.drone_docked:
            self.drone_arrival_time = time.time()
            self.drone_docked = True
        elif not drone_detected and self.drone_docked:
            self.drone_departure_time = time.time()
            self.drone_docked = False
            
        return drone_detected

    # BATTERY SWAPPING  
    def swap_battery(self):
        """
        swap drone battery with charged one
        """
        self.remove_depleted_battery()
        self.install_charged_battery()

    def remove_depleted_battery(self):
        """
        use mechanical arm to remove old battery
        """
        try:
            self.arm_position = "extracting"
            self.control_mechanical_arm("extract_battery")
            depleted_battery = self.get_battery_from_drone()
            if not depleted_battery:
                raise Exception("Failed to extract battery from drone")
            self.place_in_charging_bay(depleted_battery)
        except Exception as e:
            self.arm_position = "extraction_failed"
            # attempt to return arm to safe position
            self.control_mechanical_arm("return_to_home")
            raise

    def install_charged_battery(self):
        """
        use mechanical arm to install charged battery
        """
        try:
            self.arm_position = "installing"
            charged_battery = self.get_charged_battery_from_charging_bay()
            if not charged_battery:
                raise Exception("No charged battery available in charging bay")
            self.control_mechanical_arm("install_battery", charged_battery)
            
            # verify battery is properly installed
            if not self.verify_battery_installation():
                raise Exception("Battery installation verification failed")
                
            self.arm_position = "home"
            self.last_swap_time = time.time()
            
            battery_id = f"battery_{int}"
            self.start_charging(battery_id)
        except Exception as e:
            self.arm_position = "installation_failed"
            # log (f"Battery installation failed: e (w/ some run details)")
            # attempt to return arm to safe position
            self.control_mechanical_arm("return_to_home")
            raise

    # BATTERY CHARGING MANAGEMENT
    def start_charging(self, battery_id):
        """
        begin charging process
        once started needs continuous monitoring
        """
        try:
            self.charging_batteries[battery_id] = {
                "charge_level": int,
                "status": "charging", 
                "start_time": time.time()
            }
            self.send_charge_command(battery_id)
        except Exception as e:
            # charging system failure
            if battery_id in self.charging_batteries:
                self.charging_batteries[battery_id]["status"] = "error"
            raise

    def stop_charging(self, battery_id):
        """
        stop charging process
        """
        if battery_id in self.charging_batteries:
            self.charging_batteries[battery_id]["status"] = "complete"
        self.send_stop_charge_command(battery_id)

    def monitor_charging_batteries(self):
        """
        check status of all charging batteries
        runs continuously in background
        """
        for battery_id in list(self.charging_batteries.keys()):
            status = self.get_battery_status(battery_id)
            
            if status["charge_level"] >= 100:
                self.stop_charging(battery_id)
            elif status.get("temperature") > 60:
                # stop charging due to overheating
                self.charging_batteries[battery_id]["status"] = "overheated"
                self.send_stop_charge_command(battery_id)
            elif status.get("temperature") < 40 and status.get("status") == "overheated":
                # resume charging once temperature drops to safe level
                self.charging_batteries[battery_id]["status"] = "charging"
                self.send_charge_command(battery_id)
                

    def get_battery_status(self, battery_id):
        """
        read current battery state from management system
        """
        if battery_id in self.charging_batteries:
            battery = self.charging_batteries[battery_id]
            battery["charge_level"] = int
            battery["temperature"] = int
            return battery
        return {"charge_level": int, "status": "full"}

    # HARDWARE FUNCTIONS
    def control_mechanical_arm(self, action, battery=None):
        """arm control system"""
        pass
        
    def get_battery_from_drone(self):
        """extract battery from drone bay"""
        old_battery = self.current_drone_battery
        self.current_drone_battery = None
        return old_battery
        
    def place_in_charging_bay(self, battery):
        """find empty slot and place battery in charging bay storage slot"""
        for slot, contents in self.charging_bay_batteries.items():
            if contents is None:
                self.charging_bay_batteries[slot] = battery
                break
        
    def get_charged_battery_from_charging_bay(self):
        """retrieve charged battery from charging bay"""
        # find a charged battery in charging bay
        for slot, battery in self.charging_bay_batteries.items():
            if battery and battery in self.charging_batteries:
                if self.charging_batteries[battery].get("status", False) == "complete":
                    charged_battery = battery
                    self.charging_bay_batteries[slot] = None
                    self.current_drone_battery = charged_battery
                    return charged_battery
        # !TODO: add fallback logic if no charged battery found (idk what this would look like)
        pass
        
    def send_charge_command(self, battery_id):
        """send start charging command to battery management system"""
        pass
        
    def send_stop_charge_command(self, battery_id):
        """send stop charging command to battery management system"""
        pass
        
    def calculate_or_read_sun_angle(self):
        """read sun position or calculate sun position based on mars time and location"""
        return int
        
    def control_panel_motors(self, target_angle):
        """send commands to solar panel servo motors"""
        pass

    def activate_cleaning_brush(self):
        """activate solar panel cleaning mechanism"""
        pass
        
    def verify_battery_installation(self):
        """verify battery is properly seated and connected in drone"""
        # check electrical connection, mechanical seating, lock engagement
        return bool
        
    def send_to_gui_system(self, status):
        """send status data to monitoring gui"""
        pass

    # SOLAR PANEL OPERATIONS
    def get_sun_position(self):
        """
        calculate current sun position
        """
        calculated_angle = self.calculate_or_read_sun_angle()
        return calculated_angle

    def adjust_solar_panels(self, target_angle):
        """
        move panels to track sun
        """ 
        try:
            self.control_panel_motors(target_angle)
            self.sun_position = target_angle
        except Exception as e:
            # panel motor failure - continue operations but don't update position
            pass

    def needs_cleaning(self):
        """
        check if solar panels need cleaning
        """
        time_since_cleaning = time.time() - self.last_cleaning_time
        return time_since_cleaning > self.cleaning_interval

    def clean_solar_panels(self):
        """
        activate cleaning mechanism
        """
        try:
            self.activate_cleaning_brush()
            self.last_cleaning_time = time.time()
        except Exception as e:
            # cleaning system failure - continue operations but log issue
            pass

    # MONITORING AND STATUS
    def send_status_to_gui(self):
        """
        send system status to monitoring interface
        gui needs regular updates while other processes run
        """
        current_time = time.time()
        uptime_seconds = current_time - self.system_start_time
        uptime_hours = uptime_seconds / 3600
        
        battery_details = {}
        for battery_id, battery_info in self.charging_batteries.items():
            battery_details[battery_id] = {
                "charge_level": battery_info.get("charge_level", 0),
                "status": battery_info.get("status", "unknown"),
                "temperature": battery_info.get("temperature", 25)
            }
        
        status = {
            "timestamp": current_time,
            "datetime": time.ctime(current_time),
            "system_uptime_hours": round(uptime_hours, 2),
            "drone_docked": self.drone_docked,
            "drone_arrival_time": time.ctime if self.drone_arrival_time else "No arrivals yet",
            "drone_departure_time": time.ctime if self.drone_departure_time else "No departures yet",
            "last_swap_time": time.ctime if self.last_swap_time else "No swaps yet",
            "sun_position_degrees": self.sun_position,
            "arm_position": self.arm_position,
            "current_drone_battery": self.current_drone_battery or "None",
            "charging_bay_batteries": self.charging_bay_batteries,
            "charging_batteries_count": len(self.charging_batteries),
            "battery_details": battery_details,
            "last_cleaning_time": time.ctime,
            "time_since_cleaning_hours": int,
            "cleaning_needed": self.needs_cleaning(),
            "system_status": "running",
            "current_sequence": "monitoring" if not self.drone_docked else "battery_swap",
            "swap_status": self.swap_status
        }
        
        self.send_to_gui_system(status)
        return status

    def main_control_loop(self):
        """
        main system control loop
        
        in real implementation, these would run in parallel:
            thread1: continuous_battery_monitoring()
            thread2: continuous_sun_tracking() 
            thread3: continuous_drone_detection()
            thread4: gui_status_updates()
            main: handle_events_and_sequencing()
        """        
        while True:
            try:                
                # check for drone arrival
                if self.detect_drone():
                    try:
                        self.swap_battery()
                    except Exception as e:
                        # swap failed - reset status and continue monitoring
                        self.swap_status = "error"
                        self.arm_position = "error_recovery"
                
                # monitor ongoing processes  
                self.monitor_charging_batteries()
                
                # cleaning / maintenance 
                if self.needs_cleaning():
                    try:
                        self.clean_solar_panels()
                    except Exception as e:
                        # cleaning failed - continue
                        pass
                
                # track sun movement
                try:
                    sun_angle = self.get_sun_position()
                    self.adjust_solar_panels(sun_angle)
                except Exception as e:
                    # sun tracking failed - continue
                    pass
                
                self.send_status_to_gui()
                                
            except Exception as e:
                print(f"system error: {e}")
                break

if __name__ == "__main__":
    bay = ChargingBay()
    bay.main_control_loop()