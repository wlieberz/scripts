#!/bin/bash

# Note: doesn't check IPv6. IPv4 only.
# Basic script to check localhost for listening ports, 
# then check if there is a cert on the port and write output
# to a file to be inspected. 
# William Lieberz - June 2020. 

CurrentHost=$(hostname)

ListeningPorts=( $(sudo ss -nlptu | grep LISTEN | grep -v 127.0.0.1 | cut -d ":" -f 2 | grep -o [[:digit:]]*) )

OutFile=./$(hostname)_certs_$(date +%Y.%m.%d).txt

for p in ${ListeningPorts[@]}; do
  echo "#### PORT $p :" >> $OutFile
  CurlOutput=$(curl --insecure -v https://$CurrentHost:$p 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }' >> $OutFile)
  echo "$CurlOutput" >> $OutFile
  echo -e "\n"
  sudo lsof -i :$p >> $OutFile
  echo -e "\n"
  PortPid=$(sudo lsof -F -i :$p | grep -i p[[:digit:]] | sed 's/p//')
  sudo ps aux | grep $PortPid 2>>/dev/null 1>> $OutFile
  echo -e "\n" >> $OutFile
done

exit
