#!/usr/bin/env python3

# version: 1.0.0

# Very simple wrapper script to copy a btrfs snapshot chain
# from a source to a destination.
# 
# It worked for my simple use-case. 
# Use at your own risk!
#
# https://github.com/wlieberz/scripts

import argparse
import sys
import os
from pathlib import Path

def get_source_subvols(source_root):    
    source_subvols = sorted(Path(source_root).iterdir(), key=os.path.getmtime)    
    return source_subvols

def send_source_to_dest(source_subvols, destination, dryRun):    
    for idx, subvol in enumerate(source_subvols):
        # First snapshot doesn't have a parent:
        if idx == 0:            
            send_cmd = f"btrfs send {subvol} | btrfs receive {destination}"            
            if dryRun:
                print(f"Would do: {send_cmd}")           
            if not dryRun:                
                os.system(send_cmd)
            continue
        
        # Every other snapshot has a parent and is sent incrementally:
        parent = source_subvols[idx - 1]
        send_cmd = f"btrfs send -p {parent} {subvol} | btrfs receive {destination}"        
        if dryRun:
            print(f"Would do: {send_cmd}")      
        if not dryRun:            
            os.system(send_cmd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--dry", "-d", action='store_true')
    args = parser.parse_args()

    # Get source-subvols ordered from oldest to newest.
    source_subvols = get_source_subvols(args.source)

    if not source_subvols:
        print("[ERROR] no subvols found in source path!")
        sys.exit(1)
    
    send_source_to_dest(source_subvols, args.destination, args.dry)

if __name__ == "__main__":
    main()
