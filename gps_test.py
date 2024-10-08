# date: 08th October 2024
# contributed by : devanshj27 on github

# the code below is working on my Raspberry Pi 4B,
# the IC on gps_neo requires significant startup time,
# cold start should take ~32 seconds; then the LED on it starts blinking,
# even if the LED on the gps sensor starts blinking,
# do not expect the sensor to provide the accurate output rightaway,
# kindly wait for ~23 seconds or more, this is the warm start,
# so do not plug/insert gps sensor and immediately start running the code,
# doing so will result in code throwing an error,
# or may give (0.0, 0.0) == (latitudes, longitudes) by default unless you are on NULL island



import serial
import time
import pynmea2

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
                                                # & also shows which serial port is connected
                                                     

# if no connection was made, exit the program
if ser is None:
    print("No available GPS serial port found. Exiting.")
    exit(1)

try:
    while True:
        if ser.in_waiting > 0:
            newdata = ser.readline().decode("utf-8", errors="ignore").strip()
            if newdata.startswith("$GPGGA"):
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
#         time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    if ser is not None:
        ser.close()  # ensure the serial port is closed on exit






# date: 08th October 2024
# contributed by : devanshj27 on github

# the code below is working on my Raspberry Pi 4B,
# the IC on gps_neo requires significant startup time,
# cold start should take ~32 seconds; then the LED starts blinking,
# even if the LED on the gps sensor starts blinking,
# do not expect the sensor to provide the accurate output rightaway,
# kindly wait for ~23 seconds or more, this is the warm start,
# so do not plug/insert gps sensor and immediately start running the code,
# doing so will result in code throwing an error or receiving an unexpected output
# or may give (0.0, 0.0) == (latitudes, longitudes) by default unless you are on NULL island


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











