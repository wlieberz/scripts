#!/usr/bin/env python3

# Define a sudoers file to keep with the var: keep_file.
# Any file that isn't the keep_file will be moved to a backup dir.
# The backup dir has today's timestamp, e.g. 2021-4-23 and is created, as needed.

import os, shutil, datetime

ct = datetime.datetime.now()
year = str(ct.year)
month = str(ct.month)
day = str(ct.day)
date_stamp = f'{year}-{month}-{day}'

sudo_path = "/etc/sudoers.d"

backup_dir = f'/root/sudoers-backup_{date_stamp}'

keep_file = "special-sudos" # Customize this to your needs.

def main():
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    for entry in os.listdir(sudo_path):
        if os.path.isfile(os.path.join(sudo_path, entry)):
            if entry != keep_file:
                shutil.move(os.path.join(sudo_path, entry), backup_dir)

if __name__ == "__main__":
    main()
