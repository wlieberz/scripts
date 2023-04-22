#!/bin/bash

# Silly helper script to open an arbitrary number of 
# URLs in a browser of your choice.
# Note: Not tested with other browsers, e.g. 
# Firefox may handle args differently, etc.
# Tested on Ubuntu 22.04

# URL file should be in the format of one site per line
# Example - minus the `#` symbols:
#https://www.bing.com/
#https://duckduckgo.com/

URL_FILE="urls.txt"
BROWSER="/opt/brave.com/brave/brave"

xargs $BROWSER < $URL_FILE
