while true; do
  read LINE < /dev/ttyACM0
  python /home/pi/IsMartinRunning/MartinBot/MartinBot.py $LINE
done
