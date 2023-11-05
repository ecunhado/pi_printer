#! /bin/bash

cd /home/pi/pi_printer
/usr/bin/tmux new-session -d -s pi_printer python3 main.py --mode 0 --time 10:00
