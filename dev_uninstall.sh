#!/bin/bash

if ! [ $(id -u) = 0 ]; then
   echo "The script need to be run as root." >&2
   exit 1
fi

if [ $SUDO_USER ]; then
    real_user=$SUDO_USER
else
    real_user=$(whoami)
fi

path=`dirname $0`
rm -rf /usr/local/lib/tolino_news
rm -f /usr/local/bin/tolino_news
rm -f /usr/local/bin/tolino_news_run
echo "if you did not remove the crontab job before, you have to do it manually"
echo " you can now remove the source files in $path"
echo "you can remove calibre or epubmerge plugin if you want"

