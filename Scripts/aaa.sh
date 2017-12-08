#!/bin/bash

input=# Where to find the CSVs to use as input
output=# Where to output data
exec=# Path to trimusers.py
userids=# Path to a text file of userids. One userid per line.


months=(11-2014 12-2014 01-2015 02-2015 03-2015 04-2015 05-2015 06-2015 07-2015 08-2015 09-2015 10-2015 11-2015 12-2015 01-2016 02-2016 03-2016)

for month in ${months[*]}
do
	python3 $exec -string $month -path $input -userids $userids -output $output/aaa-$month
done
