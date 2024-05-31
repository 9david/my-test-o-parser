#!/bin/sh

rm -f /tmp/.X0-lock
# rm -f /tmp/.X99-lock

# Run Xvfb on dispaly 0.
Xvfb :0 -screen 0 1280x720x16 &

# Wait for Xvfb to start properly
sleep 2

# Run fluxbox windows manager on display 0.
fluxbox -display :0 &

# Run x11vnc on display 0
x11vnc -display :0 -forever -shared -noxdamage -nowf -ncache 10 -usepw &

# Add delay
sleep 5



