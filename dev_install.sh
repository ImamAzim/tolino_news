#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	apt install -y calibre
	mkdir -p $HOME/.config/calibre/custom_recipes
	mkdir /etc/news_loader
	cp -n "$path/news_loader/config.toml" /etc/news_loader

	wget --output-document=EpubMerge.zip https://www.mobileread.com/forums/attachment.php?attachmentid=128768&d=1663081894
	rm wget-log
	calibre-customize -a EpubMerge.zip
	rm EpubMerge.zip

	apt install -y python3-venv
	python3 -m venv /usr/local/bin/news_loader
	source /usr/local/bin/news_loader/bin/activate
	pip install $path

	cp  "$path/cron_daily_news" /etc/cron.d/

else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
