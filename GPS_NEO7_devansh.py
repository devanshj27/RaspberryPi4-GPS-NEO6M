data = None
import serial
import time
import pynmea2
gps_port = "/dev/ttyAMA0"
# gps_port = "/dev/serial0"
# gps_port = "/dev/ttyS0"

ser = serial.Serial(gps_port, 9600)


while True:
  if ser.in_waiting > 0:
    newdata = ser.readline().decode("utf-8", errors="ignore").rstrip()  ###original line
    if newdata[0:6] == "$GPGGA":
      newmsg=pynmea2.parse(newdata)
      lat=newmsg.latitude
      lng=newmsg.longitude
      gps = f" Latitude : {lat} with Longitude : {lng}"
      #gps = "Latitude = " + str(lat) + " and Longitude = " + str(lng)
      print(gps)
  time.sleep(1)




