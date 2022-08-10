#!/usr/bin/env python3

# Helper script to assist with switching from local-only auth to ldap auth.
# Remove all local accounts when the ldap account exists, but do not touch
# accounts in the exclusion_list. Then chown each user's home dir so the UID
# is updated with the LDAP UID rather than the former local UID.
# Also update /home permissions to be closer to RHEL defaults.

import os

exclusion_list = ["example-user-1", "example-user-2"]

group_owner = "example-group"

def main():
    local_user_list_raw = os.listdir('/home/')

    local_user_list = [x for x in local_user_list_raw if x not in exclusion_list]

    for item in local_user_list:
        remove_local_user_cmd = f'sed -i "/{item}/d" /etc/passwd'
        os.system(remove_local_user_cmd)

        chown_cmd = f'chown --recursive {item}:{group_owner} /home/{item}'
        os.system(chown_cmd)

        chmod_cmd = f'chmod 755 /home/{item}'
        os.system(chmod_cmd)

    print("Done.")

if __name__ == "__main__":
    main()
