#!/bin/bash

# Back-up MySQL, keeping on the latest 3 back-up files. 

# Current script removes all but the latest 3 back-up files, regardless of age.
# If we know in advance the retention period we could do something like this for the removal: 
# find $backup_path  -mindepth 1 -mtime +5 -delete


#### VARS:
# SQLDUMP PARAMS:
mysql_host="localhost"
dump_opts="--events --routines --triggers --all-databases"
mysql_username="SQLBackUpUser"
mysql_password='YourSuperSecurePassword'
backup_path=/some/backup/path

# General Vars:
timestamp=$(date +%Y-%m-%d-%H%M)

# FUNCTIONS:
function GetNumFiles {
  ls -tp $backup_path | grep -v '/$' | wc -l
}

function GetOldestFile {
  ls -tp $backup_path | grep -v '/$' | tail -n1
}

function DoBackup {
  /usr/bin/mysqldump -h $mysql_host -u $mysql_username -p$mysql_password $dump_opts > $backup_path/sqldump_$timestamp.sql
}

# FLOW CONTROL:

until [ $(GetNumFiles) -lt 3 ]; do
  rm "$backup_path/$(GetOldestFile)"
done

DoBackup

exit 0
