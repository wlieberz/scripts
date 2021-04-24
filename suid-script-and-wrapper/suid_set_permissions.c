#include "stdio.h"

void main(int argc, char const *argv[])
{
    if (argc == 2) {
        char command[100] = {0};
        setuid(0);
        sprintf(command, "/usr/local/sbin/do_suid_set_permissions.py %s", argv[1]);
        system(command);
    }

   if (argc == 1) {
       printf("Error: must include one positional parameter command line argument for baseDir. Run with -h for more info.\n");
   }
}
