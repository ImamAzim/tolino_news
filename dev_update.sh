#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`

else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
