#!/usr/bin/env python3

# v1.0.2

import os, sys, datetime, platform

# _________________________ Variables:

local_snaps_dir = "/snapshots"

dev_by_uuid = "/dev/disk/by-uuid"
backup_disk_uuid = "88946926-7c75-40da-bd50-c31c592c6591"
backup_disk_mount_point = "/mnt/external-btrfs-2"
backup_disk_checkfile = "external-btrfs-2_is-mounted.txt"

ct = datetime.datetime.now()
today_time = ct.strftime("%Y%m%d%H%M")

today_snap_path = f'{local_snaps_dir}/home-{today_time}'

# _________________________ Functions:

def check_num_local():
    global local_snapshots
    local_snapshots = os.listdir(local_snaps_dir)
    if len(local_snapshots) != 2:
        sys.exit("Exiting: there must be two local snapshots.")

def mount_backup_vol():
    mount_cmd = f'sudo mount {dev_by_uuid}/{backup_disk_uuid} {backup_disk_mount_point}'
    os.system(mount_cmd)
    if not os.path.exists(os.path.join(backup_disk_mount_point, backup_disk_checkfile)):
        sys.exit("Exiting: backup volume is not mounted.")

def get_parent_snap():
    local_snapshots_date_only = []
    for snap in local_snapshots:
        local_snapshots_date_only.append(int(snap.replace('home-', '')))
    global parent_snap
    parent_snap = "home-" + str(max(local_snapshots_date_only))
    global oldest_local_snap
    oldest_local_snap = "home-" + str(min(local_snapshots_date_only))
    print(f'Found parent snapshot: {parent_snap}')

def do_today_snap():
    today_snap_cmd = f'sudo btrfs subvolume snapshot -r /home {today_snap_path}'
    if not os.path.exists(today_snap_path):
        print("Taking today's snapshot.")
        os.system(today_snap_cmd)
    else:
       sys.exit("Exiting: today's backup already exists.")

def send_today_snap():
    send_cmd = f'sudo btrfs send -p {local_snaps_dir}/{parent_snap} {today_snap_path}'
    backup_dest = backup_disk_mount_point + '/' + platform.node().split('.', 1)[0]
    rec_cmd = f'sudo btrfs receive {backup_dest}'
    btrfs_send_today_snap = f'{send_cmd} | {rec_cmd}'
    print("Sending today's snapshot to external.")
    print(f'With command: {send_cmd} | {rec_cmd}')
    os.system(btrfs_send_today_snap)

def del_oldest_local_snap():
    print(f'Removing the oldest local snapshot: {oldest_local_snap}')
    del_oldest_local_snap_cmd = f'sudo btrfs subvolume delete {local_snaps_dir}/{oldest_local_snap}'
    os.system(del_oldest_local_snap_cmd)

def unmount_backup_vol():
    unmount_cmd = f'sudo umount {backup_disk_mount_point}'
    print("Unmounting external backup volume.")
    os.system(unmount_cmd)

def main():
    check_num_local()
    mount_backup_vol()
    get_parent_snap()
    do_today_snap()
    send_today_snap()
    del_oldest_local_snap()
    unmount_backup_vol()

if __name__ == "__main__": main()
