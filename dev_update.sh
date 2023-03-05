#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	git -C $path pull
	source /usr/local/bin/news_loader/bin/activate
	pip install $path
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
