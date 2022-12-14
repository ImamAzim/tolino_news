#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	apt install -y calibre
	cp -r "`dirname $0`/news_loader_recipes" $HOME/.config/calibre/
	wget --output-document=EpubMerge.zip https://www.mobileread.com/forums/attachment.php?attachmentid=128768&d=1663081894
	rm wget-log
	calibre-customize -a EpubMerge.zip
	rm EpubMerge.zip

	cp "`dirname $0`/load_news.py" /usr/local/bin
	chmod +x /usr/local/bin/load_news.py

	cp "`dirname $0`/send_signal.sh" /usr/local/bin
	chmod +x /usr/local/bin/send_signal.sh

	cp "`dirname $0`/50-load_news.rules" /etc/udev/rules.d/
	udevadm control --reload

	mkdir -p /mnt/ereader

	cp "`dirname $0`/load_news.service" /etc/systemd/system/
	chmod 755 /etc/systemd/system/load_news.service
	systemctl daemon-reload
	systemctl enable load_news.service

else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
