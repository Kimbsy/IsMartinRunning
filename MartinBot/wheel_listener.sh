while true; do
  read LINE < /dev/ttyACM0
  python /home/pi/MartinBot/MartinBot.py $LINE
done
