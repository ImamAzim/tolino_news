#!/bin/bash


path=`dirname $0`
wget --output-document=EpubMerge.zip https://www.mobileread.com/forums/attachment.php?attachmentid=128768&d=1663081894
rm wget-log
calibre-customize -a EpubMerge.zip
rm EpubMerge.zip

apt install -y python3-venv
python3 -m venv /usr/local/lib/news_loader
source /usr/local/lib/news_loader/bin/activate
pip install $path
ln -fs /usr/local/lib/news_loader/bin/news_loader /usr/local/bin
ln -fs /usr/local/lib/news_loader/bin/news_loader_run /usr/local/bin

