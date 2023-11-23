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

url="https://www.mobileread.com/forums/attachment.php?s=0280306cc395ea788c3be735f52d91a0&attachmentid=128768&d=1689785083"
plugin_file="attachment.php?s=0280306cc395ea788c3be735f52d91a0&attachmentid=128768&d=1689785083"
base_url="https://www.mobileread.com/forums/"
wget "$base_url$plugin_file"
sudo -u $real_user calibre-customize -a $plugin_file
rm $plugin_file

apt install -y python3-venv
python3 -m venv /usr/local/lib/news_loader
source /usr/local/lib/news_loader/bin/activate
pip install $path
ln -fs /usr/local/lib/news_loader/bin/news_loader /usr/local/bin
ln -fs /usr/local/lib/news_loader/bin/news_loader_run /usr/local/bin

