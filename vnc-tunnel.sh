#!/usr/bin/env bash

# Simple helper script to establish local ssh tunnel for vnc.
# 2020-02-26, William Lieberz

# VARIABLES:
workstation_port=8989

num_args=$#
display_number=$1
vnc_server=$2

num_re='^[0-9]+$'

# FUNCTIONS:

show_help () {
  echo "Usage: $0 <vnc display number> <vnc server>"  
}

check_args () {
    # Exit if number of args not equal to 2:
    if [[ $num_args -ne 2 ]]; then
      show_help
      exit 1
    fi

    # Exit if first arg not a number:
    if ! [[ $display_number =~ $num_re ]]; then
      echo "Error: first agument must be a number."
      show_help
      exit 2
    fi
}

do_tunnel () {
  ssh -f -T -N -L $workstation_port:localhost:590$display_number $vnc_server
  tunnel_pid=$(ps aux | grep $workstation_port | grep -v grep | cut -d' ' -f 4)
  echo "Tunnel established as PID: $tunnel_pid." 
  echo "Connect to the vnc server via localhost:$workstation_port"
}

# MAIN:

check_args

do_tunnel

exit
