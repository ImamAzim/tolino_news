#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	rm -rf $HOME/.config/calibre/news_loader_recipes
	echo " you can now remove the source files in `dirname $0`"
	echo "you can remove calibre if you want"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi

