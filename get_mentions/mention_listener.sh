# This Bash script runs the get_mentions.py script to check Twitter
# for new mentions.
# 
# Remeber that if you're pi's username is not 'pi', or if you create this
# project somewhere different, the file paths will all need to change.
# 
# Run it with the command:
#   ./mention_listener.sh
#   

while true; do
  # run the python script
  python /home/pi/IsMartinRunning/get_mentions/get_mentions.py
  # wait for 1 minute
  sleep 1m
done
