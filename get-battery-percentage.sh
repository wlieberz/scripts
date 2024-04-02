#!/usr/bin/env bash

# Note: upower has other interesting info and is worth looking at sometimes without
#  filtering (i.e., without the grep)

battery=$(upower -e | grep 'BAT')

echo "$battery"

upower -i $battery | grep percentage

exit
