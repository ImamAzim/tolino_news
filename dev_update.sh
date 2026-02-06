#!/bin/bash


path=`dirname $0`
git -C $path pull
source /usr/local/lib/tolino_news/bin/activate
pip install $path
ln -fs /usr/local/lib/tolino_news/bin/token_update /usr/local/bin
