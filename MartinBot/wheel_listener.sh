# This Bash script loops continuously trying to read data from the usb port
# attached to the wheel sensor arduino (ttyACMO).
# 
# You're serial port may well be different (e.g. ttyUSB0).
#
# Remeber that if you're pi's username is not 'pi', or if you create this
# project somewhere different, the file paths will all need to change.
#  
# Run it with the command:
#   ./wheel_listener.sh
#

while true; do
  # read a line of data (ending with a new line character "\n")
  read LINE < /dev/ttyACM0
  # let us know about it
  echo "data received"
  # run the python script with the data as an argument
  python /home/pi/IsMartinRunning/MartinBot/MartinBot.py $LINE
done
