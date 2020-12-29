#!/bin/bash

# Script to take btrfs backup and send to an external hdd (formatted as btrfs). 
# Script would need to be modified to support a backup frequency higher than once per day
# (just append the hour and minute to the timestamp). Script takes a read-only snapshot of the /home subvolume
# and removes the oldest local snapshot. No remote snapshots are removed. 
# See variables for hard-coded values which the script needs; adjust to your needs. 
# 
# -- William Lieberz 2020-12-28

# ----------- VARS ------------- #

bak_disk_uuid=a5a91dad-b079-4e64-b71a-ff86712f3d8b # Substitute with your UUID.
# If your backup disk is sdc1 you can get your uuid with: sudo blkid /dev/sdc1
bak_disk_mount_point=/mnt/external-btrfs-1
bak_disk_checkfile=external-btrfs-1_is-mounted.txt

local_snapshots_dir=/snapshots
today_timestamp=$(date +%Y%m%d) # e.g. on Dec 28 2020, looks like: 20201228

# Most recent snapshot before taking snapshot today:
parent_snapshot=$(ls -1t $local_snapshots_dir | tail -n 1)

oldest_local_snap=$(ls -1t $local_snapshots_dir | head -n 1)

# ---------- MAIN -------------- #

# Mount backup drive:
sudo mount /dev/disk/by-uuid/$bak_disk_uuid $bak_disk_mount_point 

# Sanity check mount is ok:
if [ -f "$bak_disk_mount_point/$bak_disk_checkfile" ]; then
  echo "Sanity check: Backup drive mount seems ok..."
else 
  echo "Something is wrong with the backup drive mount. Bailing!"
  exit 1
fi

echo "Using as parent snapshot: $parent_snapshot"

# Take snapshot with today's timestamp.
echo "Taking new snapshot..."
sudo btrfs subvolume snapshot -r /home $local_snapshots_dir/home-$today_timestamp

# Send today's snapshot with the next most recent as the parent to the external drive: 
echo "Sending new snapshot to external drive..."
sudo btrfs send -p $local_snapshots_dir/$parent_snapshot $local_snapshots_dir/home-$today_timestamp | sudo btrfs receive $bak_disk_mount_point/$(hostname -s)

# Remove the oldest local snapshot.
echo "Removing oldest local snapshot: $oldest_local_snap"
sudo btrfs subvolume delete $local_snapshots_dir/$oldest_local_snap

# Unmount the backup drive.
echo "Unmounting back-up drive."
sudo umount /dev/disk/by-uuid/$bak_disk_uuid

echo "All done."

exit 
