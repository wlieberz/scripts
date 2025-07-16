# About

This is a cheatsheet for mounting your Android phone storage via MTP (Media Transfer Protocol) on a Linux host via a FUSE mount
for handy CLI access.

This is mostly relevant on KDE, since Gnome and other desktop environments using Gnome components (e.g. XFCE)
can use GVFS (Gnome Virtual Filesystem), which is most excellent.

Note: if you are happy using the GUI, KDE can handle Android MTP access via the normal file browser (Dolphin),
and you do not need any of this. In fact, you can normally go to Dolpin and type in the location bar `mtp://` and
you will see any MTP devices that KDE is aware of.

Unfortunately, and unlike Gnome's GVFS, while KDE's KIO backend will make
the MTP pseudo filesystem available to you in Dolpin and probably certain other KDE apps, it isn't made available
to a terminal, as far as I can determine. No, not even Konsole. I'm not a Gnome fan, but GVFS is pretty great.

Essentially this quick write-up and sample scripts can get you an experience similiar to gvfs-mtp for CLI access
to an MTP storage device on KDE without needing to install any Gnome components.

## Requirements

You will need the binary `aft-mtp-mount`. On Fedora, this is provided by the `android-file-transfer` package.

```sh
sudo dnf install -y android-file-transfer
```

## Usage

Assuming you have copied this `mtp-kit` directory into your $HOME:

```sh
cd ~/mtp-kit/

./mount-phone.sh

# then, when done:
./unmount-phone.sh
```

Sometimes native KDE processes will "grab" the MTP device so that `mount-phone.sh` will fail. In such a case, try `release-mtp-kio.sh`. Use at your own risk.


