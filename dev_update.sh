#!/bin/bash


path=`dirname $0`
git -C $path pull
source /usr/local/lib/tolino_news/bin/activate
pip install $path
