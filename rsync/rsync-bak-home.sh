#!/usr/bin/env bash

# ----------- VARS ------------- #

bak_disk_uuid=88946926-7c75-40da-bd50-c31c592c6591 # Substitute with your UUID.
bak_disk_mount_point=/mnt/external-btrfs-2
bak_disk_checkfile=external-btrfs-2_is-mounted.txt

rsyncOpts="--verbose --recursive --links --perms \
--executability --owner --group --times --delete \
--exclude=.cache --human-readable --progress"

bakDest=$bak_disk_mount_point/$(hostname -s)/$HOME

# ----------- MAIN ------------- #

# Mount backup drive:
sudo mount /dev/disk/by-uuid/$bak_disk_uuid $bak_disk_mount_point

# Sanity check mount is ok:
if [ -f "$bak_disk_mount_point/$bak_disk_checkfile" ]; then
  echo "Sanity check: Backup drive mount seems ok..."
else 
  echo "Something is wrong with the backup drive mount. Bailing!"
  exit 1
fi

# Do the back-up:
rsync $rsyncOpts $HOME/ $bakDest/

# Unmount the backup drive.
echo "Unmounting back-up drive."
sudo umount /dev/disk/by-uuid/$bak_disk_uuid

echo "Last back-up: $(date)" | tee $HOME/last-backup.txt

exit 