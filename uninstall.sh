#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	#rm -rf $HOME/.config/calibre/news_loader_recipes
	calibre-customize -r EpubMerge
	#rmdir /mnt/ereader
	#rm /etc/systemd/system/mnt-ereader.mount
	rm /etc/systemd/system/load_news.service
	systemctl daemon-reload
	#rm /etc/udev/rules.d/50-automountusb.rules
	#udevadm control --reload
	rm /usr/local/bin/load_news.py
	echo " you can now remove the source files in `dirname $0`"
	echo "you can remove calibre if you want"
	echo "you can remove you recipe and credentials in $HOME/.config/calibre/news_loader_recipes"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi

