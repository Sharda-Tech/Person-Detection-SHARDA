
#! /bin/bash

printf "%-15s%15s\n" "TIMESTAMP" "TEMP(degC)"
printf "%20s\n" "-----------------"

while true
do
	temp=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
	timestamp=$(date)
	printf "%-15s%5s\n" "$timestamp" "$temp"
	sleep 1
done
