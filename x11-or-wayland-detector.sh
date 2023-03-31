#!/bin/bash

# use loginctl to display if the current session is x11 or wayland
# tested on kubuntu 22.04

# get the session-id of the current user
SESH_ID=$(loginctl | grep $USER | awk '{ print $1 }')

# show the type
loginctl show-session $SESH_ID -p Type
