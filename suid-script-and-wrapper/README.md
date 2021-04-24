# About

I wrote the Python script and C program to assist with the modernization efforts around some legacy software which requires root permissions on some modules to run properly. 

While the CI/CD pipeline was being built, developers were constantly needing to ask System Admins to change permission on certain files. I wrote these scripts as a stop-gap measure to allow the developers to set the required permissions in a self-service manner without needing any sudo rights.

From the Python script:

This allows a user without any root privileges to set a given number of files with
root:root 4775 ownerhip / permissions.
The user can specify the baseDir, which will be inserted into the otherwise hard-coded paths.
For example, the user runs: suid_set_permissions V5.1
which would set the permissions on: /home/customApp/V5.1/SOFTWARE/modules/file1
and the rest of the files specified in the list "files".
This python script is called by a compiled C program wrapper: suid_set_permissions which 
itself has root suid.

### Deployment

The compiled C program and python script should be copied to `/usr/local/sbin/` on the remote server with the following permissions:

```

-rwxrwxr--. 1 root root  do_suid_set_permissions.py
-r-sr-x---. 1 root devs  suid_set_permissions

```

Thus only users in the devs group can run: `suid_set_permissions <base dir>` which will run as root and call `do_suid_set_permissions.py`. 

Important: be sure regular users cannot modify the contents of `do_suid_set_permissions.py'.


William Lieberz
April 23, 2021