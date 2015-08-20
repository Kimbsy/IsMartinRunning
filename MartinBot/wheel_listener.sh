while true; do
  read LINE < /dev/ttyACM0
  echo "data received"
  python /home/pi/IsMartinRunning/MartinBot/MartinBot.py $LINE
done
