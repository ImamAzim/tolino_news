#!/bin/bash


if [ $UID = 0 ]
then
	path=`dirname $0`
	apt install -y calibre
	cp "`dirname $0`/news_loader_recipes" $HOME/.config/calibre/
	wget https://www.mobileread.com/forums/attachment.php?attachmentid=128768&d=1663081894
	calibre-customize -a EpubMerge.zip
else
	echo "please run this script as root. create one if necessary with the command:
	sudo passwd root"
fi
