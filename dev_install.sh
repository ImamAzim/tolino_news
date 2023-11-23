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
python3 -m venv /usr/local/lib/news_loader
source /usr/local/lib/news_loader/bin/activate
pip install $path
ln -fs /usr/local/lib/news_loader/bin/news_loader /usr/local/bin
ln -fs /usr/local/lib/news_loader/bin/news_loader_run /usr/local/bin

