#!/usr/bin/env python3

# Author: William Lieberz
# Date: 2021-07-27
# Version: 1.0
#
# Description:
# Simple script to parse output of ansible-playbook.
# 1) Run ansible-plabook and save the output, e.g.:
#   ansible-playbook test-playbook.yml | tee test-playbook_output_2021-07-27.txt
# 2) Run script, pointing it to the file you want to parse:
#   ./parse-ansible-playbook-output.py -f test-playbook_output_2021-07-27.txt
# It will generate 5 files, each with a list of hosts separated by newlines:
#     test-playbook_output_2021-07-27.txt_parsed_failures.txt
#     test-playbook_output_2021-07-27.txt_parsed_fully_successful.txt
#     test-playbook_output_2021-07-27.txt_parsed_reachable.txt
#     test-playbook_output_2021-07-27.txt_parsed_summary.txt
#     test-playbook_output_2021-07-27.txt_parsed_unreachable.txt
# The summary file might be the most interesting. Sample output:
#     Total hosts tried: 8449
#     Reachable hosts: 6023
#     Unreachable hosts: 2426
#     Fully successful hosts: 6011
#     Hosts with failures (reachable): 12

import argparse

def main():
    # Set-up cli args:
    parser = argparse.ArgumentParser(description='Summarize Ansible playbook output.')
    parser.add_argument('--file', '-f', help='File to parse.', required=True)    
    args = parser.parse_args()
    
    # Set-up empty lists:
    unreachable_hosts = []
    reachable_hosts = []
    fully_successful_hosts = []
    failure_hosts = []
  
    with open(args.file, 'r') as parse_file:    
        for line in parse_file:
            # Categorize unreachable hosts:
            if 'unreachable=1' in line:
                # Append hostname to list by splitting on spaces.
                unreachable_hosts.append(line.split()[0])
            # Categorize reachable hosts:
            if 'unreachable=0' in line:            
                reachable_hosts.append(line.split()[0])
            # Categorize fully successful hosts:
            if 'failed=0' in line and 'unreachable=0' in line:            
                fully_successful_hosts.append(line.split()[0])
            # Categorize hosts with failures:
            if 'failed=' in line and 'failed=0' not in line:
                failure_hosts.append(line.split()[0])

    
    # Calculate summary data:    
    total_unreachable_hosts = len(unreachable_hosts)
    total_reachable_hosts = len(reachable_hosts)
    total_hosts = total_unreachable_hosts + total_reachable_hosts
    total_successful_hosts = len(fully_successful_hosts)
    total_failure_hosts =  len(failure_hosts)
    
    # Write summary data:
    summary_file_name = args.file + "_parsed_summary.txt"
    with open(summary_file_name, 'w') as summary_file:
        summary_file.write(f'Total hosts tried: {total_hosts}\n')
        summary_file.write(f'Reachable hosts: {total_reachable_hosts}\n')
        summary_file.write(f'Unreachable hosts: {total_unreachable_hosts}\n')
        summary_file.write(f'Fully successful hosts: {total_successful_hosts}\n')
        summary_file.write(f'Hosts with failures (reachable): {total_failure_hosts}\n')

    # Write sorted unreachable hosts:
    unreachable_file_name = args.file + "_parsed_unreachable.txt"
    with open(unreachable_file_name, 'w') as unreachable_file:
        unreachable_hosts_sorted = sorted(unreachable_hosts)
        for host in unreachable_hosts_sorted:
            unreachable_file.write(f'{host}\n')

    # Write sorted reachable hosts:
    reachable_file_name = args.file + "_parsed_reachable.txt"
    with open(reachable_file_name, 'w') as reachable_file:
        reachable_hosts_sorted = sorted(reachable_hosts)
        for host in reachable_hosts_sorted:
            reachable_file.write(f'{host}\n')

    # Write sorted fully-successful hosts:
    fully_successful_file_name = args.file + "_parsed_fully_successful.txt"
    with open(fully_successful_file_name, 'w') as fully_successful_file:
        fully_sucessful_hosts_sorted = sorted(fully_successful_hosts)
        for host in fully_sucessful_hosts_sorted:
            fully_successful_file.write(f'{host}\n')

    # Write sorted failure hosts:
    failures_file_name = args.file + "_parsed_failures.txt"
    with open(failures_file_name, 'w') as failures_file:
        failure_hosts_sorted = sorted(failure_hosts)
        for host in failure_hosts_sorted:
            failures_file.write(f'{host}\n')
       

if __name__ == "__main__":
    main()