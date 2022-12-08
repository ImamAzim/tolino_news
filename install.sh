#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	apt install -y calibre
	cp "`dirname $0`/news_loader_recipes" $HOME/.config/calibre/
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
