#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	calibre-customize -r EpubMerge
	rm /etc/systemd/system/load_news.service
	rm /etc/systemd/system/mnt-ereader.mount
	systemctl daemon-reload
	rm /etc/udev/rules.d/50-load_news.rules
	udevadm control --reload
	rm /usr/local/bin/load_news.py
	rm /usr/local/bin/send_signal.sh
	echo " you can now remove the source files in `dirname $0`"
	echo "you can remove calibre if you want"
	echo "you can remove you recipe and credentials in $HOME/.config/calibre/news_loader_recipes"
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi

