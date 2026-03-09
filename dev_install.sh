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

apt install -y python3-venv
apt install -y libxkbcommon0
apt install -y libglx0
apt install -y libopengl0
apt install -y xvfb
apt install -y chromium
python3 -m venv /usr/local/lib/tolino_news
source /usr/local/lib/tolino_news/bin/activate
pip install $path
ln -fs /usr/local/lib/tolino_news/bin/tolino_news /usr/local/bin
ln -fs /usr/local/lib/tolino_news/bin/token_update /usr/local/bin
ln -fs /usr/local/lib/tolino_news/bin/tolino_news_run /usr/local/bin
echo "install complete!"
echo "you need to install now calibre if it is not present"
echo "then you can run tolino_news from any user and configure"
