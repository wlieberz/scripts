#!/usr/bin/env python3

# v2.0.0

import json
import os
import sys
import datetime
import platform
import subprocess

def check_num_local(conf):
    local_snapshots = os.listdir(conf["local_snaps_dir"])
    return local_snapshots

def mount_backup_vol(conf):
    mount_cmd = f'sudo mount {conf["dev_by_uuid"]}/{conf["backup_disk_uuid"]} {conf["backup_disk_mount_point"]}'

    ret_val = subprocess.call(mount_cmd, shell=True)
    if ret_val != 0:
        sys.exit("[FATAL] Unable to mount backup volume.")

    checkfile = os.path.join(conf["backup_disk_mount_point"], conf["backup_disk_checkfile"])
    if not os.path.exists(checkfile):
        sys.exit("[FATAL]: backup volume is not mounted.")

def get_parent_snap(local_snapshots):
    local_snapshots_date_only = []

    for snap in local_snapshots:
        local_snapshots_date_only.append(int(snap.replace('home-', '')))

    parent_snap = "home-" + str(max(local_snapshots_date_only))

    oldest_local_snap = "home-" + str(min(local_snapshots_date_only))

    return parent_snap, oldest_local_snap

def do_today_snap(today_snap_path):
    today_snap_cmd = f'sudo btrfs subvolume snapshot -r /home {today_snap_path}'

    if os.path.exists(today_snap_path):
        sys.exit("[FATAL] Today's backup already exists.")

    print("[INFO] Taking today's snapshot.")

    ret_val = subprocess.call(today_snap_cmd, shell=True)
    if ret_val != 0:
        sys.exit("[FATAL] Unable to do_today_snap.")

def send_today_snap(conf, parent_snap, today_snap_path):
    send_cmd = f'sudo btrfs send -p {conf["local_snaps_dir"]}/{parent_snap} {today_snap_path}'

    short_hostname = platform.node().split('.', 1)[0]
    backup_dest = conf["backup_disk_mount_point"] + '/' + short_hostname

    rec_cmd = f'sudo btrfs receive {backup_dest}'

    send_today_snap_cmd = f'{send_cmd} | {rec_cmd}'

    print(f"[INFO] Sending today's snapshot to external with command: {send_today_snap_cmd}")

    ret_val = subprocess.call(send_today_snap_cmd, shell=True)
    if ret_val != 0:
        sys.exit("[FATAL] Unable to send today's snapshot.")

def del_oldest_local_snap(conf, oldest_local_snap):
    print(f'[INFO] Removing the oldest local snapshot: "{oldest_local_snap}".')

    del_oldest_local_snap_cmd = f'sudo btrfs subvolume delete {conf["local_snaps_dir"]}/{oldest_local_snap}'

    ret_val = subprocess.call(del_oldest_local_snap_cmd, shell=True)
    if ret_val != 0:
        sys.exit("[FATAL] Unable to delete the oldest local snapshot.")

def unmount_backup_vol(conf):
    unmount_cmd = f'sudo umount {conf["backup_disk_mount_point"]}'

    print(f'[INFO] Unmounting external backup volume: "{conf["backup_disk_mount_point"]}"')

    ret_val = subprocess.call(unmount_cmd, shell=True)
    if ret_val != 0:
        sys.exit("[FATAL] Unable to unmount the backup volume.")

def main():
    # Get config:
    conf_file_name = "btrfs-backup-conf.json"

    if not os.path.exists(conf_file_name):
        sys.exit(f'Unable to find config file: {conf_file_name}')

    conf_file = open(conf_file_name)
    conf = json.load(conf_file)
    conf_file.close()

    ct = datetime.datetime.now()
    today_time = ct.strftime("%Y%m%d%H%M")
    today_snap_path = f'{conf["local_snaps_dir"]}/home-{today_time}'

    # Do backup tasks:
    local_snapshots = check_num_local(conf)
    if len(local_snapshots) != 2:
        sys.exit("[FATAL]: there must be two local snapshots.")

    mount_backup_vol(conf)

    parent_snap, oldest_local_snap = get_parent_snap(local_snapshots)
    print(f'[INFO] Found parent snapshot: {parent_snap}')

    do_today_snap(today_snap_path)

    send_today_snap(conf, parent_snap, today_snap_path)

    del_oldest_local_snap(conf, oldest_local_snap)

    unmount_backup_vol(conf)

    print("[INFO] Completed successfully.")

if __name__ == "__main__":
    main()
