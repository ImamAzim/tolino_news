News Loader
============
a daemon to install on a raspberry pi. every day at 06:35, it will automatically fetch news and transfer them to a selected webdav folder

Status
======
on developpement.

Installlation
==============
#. clone project
#. run install.sh
#. change password and username in reveil.recipe
#. create webdav shared folder
#. put webdavlink and credential in $HOME/.config/calibre/news_loader/webdav.json
#. reboot

customization
==============
you can change the recipes, remove or add some. if necessary create a .credential file with the same structure as the current one.
