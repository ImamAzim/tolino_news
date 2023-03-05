#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	calibre-customize -r EpubMerge
	rm -rf /usr/local/bin/news_loader
	echo " you can now remove the source files in `dirname $0`"
	echo "you can remove calibre if you want"
	echo "you can remove you recipe and credentials in $HOME/.config/calibre/news_loader_recipes"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi

