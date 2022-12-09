#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	cp "`dirname $0`/load_news.py" /usr/local/bin
	chmod +x /usr/local/bin/load_news.py

else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
