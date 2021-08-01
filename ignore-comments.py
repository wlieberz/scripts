#!/usr/bin/env python3

# Dead simple utility:
# strips a file of any lines which begin with #.

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='File to process.')
    # Show help if at least one argument not given:
    if len(sys.argv) ==  1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
        
    if args.file:        
        with open(args.file, 'r') as parse_file:
            for line in parse_file:
                current_line = line.rstrip()
                if current_line.startswith("#"):
                    continue
                print(current_line)


if __name__ == "__main__":
    main()