import serial
import time
import pynmea2

import RPi.GPIO as GPIO
import time

import datetime

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
Buzzer = 21
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.output(Buzzer, False)

def buzzer():
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    Buzzer = 21
    GPIO.setup(Buzzer, GPIO.OUT)
    GPIO.output(Buzzer, False)
#         print("Buzzer OFF")
    time.sleep(5.5)
    GPIO.output(Buzzer, True)
#         print("Buzzer ON")
    time.sleep(0.1)
    GPIO.output(Buzzer, False)
#         print("Buzzer OFF")
    time.sleep(0.01)
    GPIO.output(Buzzer, True)
#         print("Buzzer ON")
    time.sleep(0.1)



# List of possible serial ports on Raspberry Pi 4B
gps_ports = ["/dev/ttyS0", "/dev/serial0", "/dev/ttyAMA0"]
ser = None

for port in gps_ports: # try and except is implemented to connect to one of the serial ports
                       # and also to avoid errors by better handling the exceptions
                       # since it has been observed that the serial ports have been different
                       # with varying setup
    try:
        ser = serial.Serial(port, 9600, timeout = 1)  # set a timeout for the connection
        print(f"Connected to {port}")
        break  # this will exit the loop only if the connection is successful
    except (serial.SerialException, OSError) as e:
        continue
#         print(f"Failed to connect to {port}: {e}") # use this line for debugging, 
                                                     # incase the code throws an error,
                                                # & also shows which serial port is not connected
                                                     

# if no connection was made, exit the program
if ser is None:
    print("No available GPS serial port found. Exiting.")
    exit(1)

# Get current date and time
now = datetime.datetime.now()
try:
    while True:
        if ser.in_waiting > 0:


            newdata = ser.readline().decode("utf-8", errors="ignore").strip()
            if newdata.startswith("$GPGGA"):
                try:
                    now2 = datetime.datetime.now()
                    running = now2 - now
                    newmsg = pynmea2.parse(newdata)
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = f"Latitude: {lat} with Longitude: {lng}"
                    if max(lat,lng) > 0:
                        buzzer()
                    
                    now2 = datetime.datetime.now()
                    times = now2 - now
                    print(gps, times)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}", running)
                except AttributeError:
                    print("Parsed message does not contain latitude/longitude.", running)
#         time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    if ser is not None:
        ser.close()  # ensure the serial port is closed on exit






# date: 08th October 2024
# contributed by : devanshj27 on github

# the code below is working properly,
# the IC on gps_neo requires significant startup time upto ~90 seconds or more,
# even if the LED on the gps sensor starts blinking,
# do not expect the sensor to provide the accurate output rightaway,
# kindly wait for ~25 seconds or more,
# so do not plug/insert gps sensor and immediately start running the code,
# doing so will result in code throwing an error,
# or may give (0.0, 0.0) == (latitudes, longitudes) by default,
# unless you are on NULL island


'''
import serial
import time
import pynmea2

gps_port = "/dev/ttyAMA0"  # Adjust this as needed
ser = serial.Serial(gps_port, 9600)

try:
    while True:
        if ser.in_waiting > 0:
            newdata = ser.readline().decode("utf-8", errors="ignore").strip()  # Use strip() instead of rstrip()
            if newdata.startswith("$GPGGA"):  # More Pythonic way to check the start of the string
                try:
                    newmsg = pynmea2.parse(newdata)
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = f"Latitude: {lat} with Longitude: {lng}"
                    print(gps)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")
                except AttributeError:
                    print("Parsed message does not contain latitude/longitude.")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    ser.close()  # Ensure the serial port is closed on exit

'''

### end of code ### 08th October 2024











