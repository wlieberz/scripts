# About

The btrfs-backup-script.py is an extremely simple Python convenience wrapper around btrfs commands to take snapshots of your `/home` subvolume, and send the snapshots to a remote disk.

The remote disk is assumed to be available by mounting via `sudo mount /dev/disk/by-uuid"/YOUR-UUID`.

The script will mount the backup-disk, take a snapshot, send the snapshot to the remote disk as an incremental with the previous local snapshot as the parent, and then delete the oldest local snapshot and unmount the backup volume. If any of these steps fail, the script exits with a fatal error indicating which step failed.

You can configure where local snapshots are stored. You currently cannot configure which subvolumes to snapshot and send (hard-coded to `/home`).

You should probably not use this script for any purpose, and should instead use a better supported btrfs backup tool. Use at your own risk.

## Assumptions / Limitations

- The subvolume to be snapshotted is currently hard-coded to `/home`.
- It is assumed that there already are two local snapshots. 
- If you don't have any local snapshots, you will need to manually start the snapshot chain.
- The script will keep two local snapshots at all times.
- Snapshots are named with the format: `home-202204171920` aka `home-YYYYmmDDhhMM`.
    - `home-202204171920` == a snapshot of `/home` taken on: March 17, 2022 at 7:20 pm.
- Snapshot time resolution is 1 minute. As such, you must wait at least 1 minute between snapshots.
- Note: The timestamp of the snapshot is calculated at the beginning of the script execution.
- This script has only been tested on Ubuntu 20.04.4 LTS and OpenSUSE Leap 15.3.
- A config file `btrfs-backup-conf.json` is required to be present in the same directory as this script.

## Usage

First, ensure you have `btrfs-backup-conf.json` in the same directory as the script and has been customized to your needs. 

Ensure you have a checkfile present on your remote disk. This is just a sanity check to verify that the remote disk is correctly mounted.

Your `local_snaps_dir` must also exist.

The `local_snaps_dir` must contain exactly two local snapshots in the supported naming format (see "Assumptions / Limitations", above).

### btrfs-backup-conf.json Notes:

```
  "local_snaps_dir"         : "/snapshots", # <- default value, feel free to change.
  "dev_by_uuid"             : "/dev/disk/by-uuid", # <- should not need to change.
  "backup_disk_uuid"        : "YOUR UUID HERE", # <- Need to change this.
  "backup_disk_mount_point" : "/mnt/your-backup-disk-friendly-name",
  "backup_disk_checkfile"   : "your-backup-disk_is-mounted.txt"
```

For the `backup_disk_uuid`, if your backup location is at `/dev/sdb1`, you can get the UUID via: 

`sudo blkid /dev/sdb1`

Ensure you have Python 3.8.10 or newer.

### Run it

With all this in place, run it:

```bash
./btrfs-backup-script.py
```