#!/bin/bash

# Basic script to check a given website for hsts.
# aka HTTP Strict Transport Security.
# William Lieberz Dec 2020.

script_name=$0

usage () {
    echo "usage: $script_name -s www.site-you-want-to-check.com"
    echo "  -s --site Specify the site you want to check. "
    echo "  -e --example Show example output of site which has hsts enabled."
    echo "  -h --help Display this help and exit."
    exit 
}

example_site="www.usbank.com" # This site definitely has hsts enabled

check_site () {
  echo "Checking $site:"
  curl -s -D- https://$site/ | grep -i Strict
}


if [[ $# -eq 0 ]]; then    
    usage
    exit 2
fi


while [ "$1" != "" ]; do
    case $1 in
        -s | --site )           shift
                                site="$1"
                                check_site
                                exit
                                ;;
        -e | --example )        site=$example_site
                                check_site
                                exit
                                ;;
        -h | --help )           usage                                
                                ;;
        * )                     usage                                
    esac
    shift
done
