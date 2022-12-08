#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	apt install -y calibre
	cp "`dirname $0`/news_loader_recipes" $HOME/.config/calibre/
	cp "`dirname $0`/load_news.py" /usr/local/bin
	chmod +x /usr/local/bin/load_news.py
	wget https://www.mobileread.com/forums/attachment.php?attachmentid=128768&d=1663081894
	calibre-customize -a EpubMerge.zip

	mkdir -p /mnt/ereader
	cp "`dirname $0`/mnt-ereader.mount" /etc/systemd/system/
	chmod 755 /etc/systemd/system/mnt-ereader.mount
	systemctl daemon-reload

	cp "`dirname $0`/50-automountusb.rules" /etc/udev/rules.d/
	udevadm control --reload

	cp "`dirname $0`/load_news.service" /etc/systemd/system/
	chmod 755 /etc/systemd/system/load_news.service
	systemctl daemon-reload

else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
