#!/bin/bash


path=`dirname $0`
git -C $path pull
source /usr/local/lib/news_loader/bin/activate
pip install $path
