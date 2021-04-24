#!/usr/bin/env python3
import argparse, os, sys, stat

# This allows a user without any root privileges to set a given number of files with
# root:root 4775 ownerhip / permissions.
# The user can specify the baseDir, which will be inserted into the otherwise hard-coded paths.
# For example, the user runs: suid_set_permissions V5.1
# which would set the permissions on: /home/customApp/V5.1/SOFTWARE/modules/file1
# and the rest of the files specified in the list "files".
# This python script is called by a compiled C program wrapper: suid_set_permissions which 
# itself has root suid.

def get_baseDir():
    parser = argparse.ArgumentParser(description='Set permissions for custom application.')

    parser.add_argument('Dir',
                    metavar='baseDir',
                    type=str,
                    help='The base dir which will be inserted into: /home/customApp/baseDir/...')
    
    args = parser.parse_args()
    global baseDir
    baseDir = args.Dir
            
def set_perms():
    customApp = "/home/customApp"
    
    files = [
        "SOFTWARE/modules/file1",
        "SOFTWARE/modules/file2",
        "SOFTWARE/modules/file3",
        "SOFTWARE/modules/func_x",
        "SOFTWARE/modules/func_y",
        "SOFTWARE/bin/reader",
        "SOFTWARE/bin/gui",
        "SOFTWARE/src/mod_y",
    ] 

    for file in files:
        currentPath = os.path.join(customApp, baseDir, file)        
        # Set owner & group to root:
        os.chown(currentPath, 0, 0)
        # Set permissions as: suid u=rws g=rwx o=r-x aka 4775:       
        os.chmod(currentPath, 0o4775)
    
    print("Done.")

def main():
    get_baseDir()
    set_perms()

if __name__ == "__main__": main()