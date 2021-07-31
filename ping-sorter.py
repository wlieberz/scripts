#!/usr/bin/env python3

# Author: William Lieberz
# Date: 2021-07-30
# Version: 1.0
#
# Description:
# Simple helper utility. Given a file with one hostname per line, 
# this script attempts a dns lookup on each host. 
# If the dnslookup succeeds, it tries to ping the host.
# Example:
# ./ping-sorter.py -f test-hosts
# Outputs files:
#     test-hosts_pingsort_bad-dns.txt
#     test-hosts_pingsort_bad-ping.txt
#     test-hosts_pingsort_good.txt
#     test-hosts_pingsort_summary.txt
# Example of contents of summary file:
#     Total hosts checked: 9
#     Good hosts: 3
#     Hosts with bad DNS: 3
#     Hosts with bad ping: 3
# Notes:
#   - Only expected to work on Linux.
#   - Requires nslookup is installed and in $PATH.
#   - Time information: Was able to check 2,426 hosts in 6m26.262s


import argparse
import subprocess

def main():
    # Set-up cli args:
    parser = argparse.ArgumentParser(description='Outputs list of pingable/unpingable hosts.')
    parser.add_argument('--file', '-f', help='File to parse.', required=True)    
    args = parser.parse_args()
    
    # Vars:    
    bad_dns_hosts = []
    bad_ping_hosts = []
    good_hosts = []  
    
    with open(args.file, 'r') as parse_file:    
        for host in parse_file:
            lookup_query = ["nslookup", host.rstrip()]
            dns_lookup = subprocess.run(lookup_query)
            if dns_lookup.returncode != 0:
                bad_dns_hosts.append(host.rstrip())
                continue
            ping_cmd = ["/usr/bin/ping", "-q", "-W 1", "-c 1", host.rstrip()]
            ping_action = subprocess.run(ping_cmd)
            if ping_action.returncode == 0:
                good_hosts.append(host.rstrip())
                continue
            if ping_action.returncode > 0:
                bad_ping_hosts.append(host.rstrip())

    # Get summary data:
    good_hosts_count = len(good_hosts)
    bad_dns_hosts_count = len(bad_dns_hosts)
    bad_ping_hosts_count = len(bad_ping_hosts)
    hosts_count = good_hosts_count + bad_dns_hosts_count + bad_ping_hosts_count

    # Write summary data:
    summary_file_name = args.file + "_pingsort_summary.txt"
    with open(summary_file_name, 'w') as summary_file:
        summary_file.write(f'Total hosts checked: {hosts_count}\n')
        summary_file.write(f'Good hosts: {good_hosts_count}\n')
        summary_file.write(f'Hosts with bad DNS: {bad_dns_hosts_count}\n')
        summary_file.write(f'Hosts with bad ping: {bad_ping_hosts_count}\n')

    # Write sorted good hosts:
    good_hosts_file_name = args.file + "_pingsort_good.txt"
    with open(good_hosts_file_name, 'w') as good_file:
        good_hosts_sorted = sorted(good_hosts)
        for server in good_hosts_sorted:
            good_file.write(f'{server}\n')

    # Write bad_dns_hosts:
    bad_dns_hosts_file_name = args.file + "_pingsort_bad-dns.txt"
    with open(bad_dns_hosts_file_name, 'w') as bad_dns_file:
        bad_dns_hosts_sorted = sorted(bad_dns_hosts)
        for server in bad_dns_hosts_sorted:
            bad_dns_file.write(f'{server}\n')

    # Write bad_ping_hosts:
    bad_ping_hosts_file_name = args.file + "_pingsort_bad-ping.txt"
    with open(bad_ping_hosts_file_name, 'w') as bad_ping_file:
        bad_ping_hosts_sorted = sorted(bad_ping_hosts)
        for server in bad_ping_hosts_sorted:
            bad_ping_file.write(f'{server}\n')


if __name__ == "__main__":
    main()