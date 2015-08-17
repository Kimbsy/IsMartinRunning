while true; do
  read LINE < /dev/ttyUSB0
  python /home/pi/htd_sensor/htd_data.py $LINE
done
