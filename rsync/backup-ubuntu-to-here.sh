#!/bin/bash

# Basic rsync script to pull files from an older Ubuntu workstation
# to current Ubuntu workstation.
# William Lieberz June 2020.

ubuntu=192.168.15.4

backup_user="wlieberz"
src=$ubuntu:/home/wlieberz/
dst=/home/wlieberz/

exclude_file=/home/wlieberz/backup-ubuntu-to-here.exclude

rsync_opts="-v -r --links --perms --executability --owner --group \
--times --human-readable --progress --exclude-from=$exclude_file"

/usr/bin/rsync $rsync_opts $backup_user@$src $dst

exit
