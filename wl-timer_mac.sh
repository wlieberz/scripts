#!/usr/bin/env bash

# I couldn't find a dead-simple timer app for MacOS that I liked so I made one in bash
# This has been tested on: macOS Monterey

# Note: If the notification fires and instantly disappears, this can be fixed in:
# System Preferences > Notifications and Focus >  In the left-hand panel: Script Editor :
# "Allow Notifications" toggle should be enabled
# Script Editor alert style should be: "Alerts"
# This configuration will set the notification to stay on-screen until dismissed.

if [[ ! $OSTYPE == "darwin"* ]]; then
    echo "[ERROR] Only MacOS is supported"
    exit 1
fi

function show_usage {
  echo "    USAGE:"
  echo "        $0 5m"
  echo "        Timer duration must be specified in minutes, e.g.: 1m"
}

# Check number of parameters is expected (1):
if [[ "$#" -ne 1 ]]; then
    echo "[ERROR] Illegal number of parameters"
    show_usage
    exit 1
fi

# Check timer_duration is a supported format:
timer_duration=$1

supported_format='[:digit:]?m'

if [[ ! $timer_duration =~ $supported_format ]]; then
    echo "[ERROR] invalid timer duration"
    show_usage
    exit 1
fi

# Convert minute duration into seconds for BSD sleep:
#
# Strip the "m" from the string, e.g.: 5m -> 5
duration_no_m=$(echo $timer_duration | sed s/m//)
#
# Convert to seconds:
duration_seconds=$((duration_no_m * 60))

# Sleep and send notification:
sleep $duration_seconds

# Date format example: 01:08 PM
timer_done_timestamp=$(date "+%I:%M %p")

osascript -e "display notification \"$timer_duration timer done at $timer_done_timestamp\" with title \"WL Timer\""

exit
