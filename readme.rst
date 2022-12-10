News Loader
============
a daemon to install on a raspberry pi. Once you connect your ereader, it will automatically fetch news and transfer them to ereader

Status
======
on developpement.

Installlation
==============
#. clone project
#. run install.sh
#. change ereader name
#. set device id and manuf id in udev rules
#.  udevadm control --reload
#. uid (blkid) in mnt-ereader.mount
#. systemctl daemon-reload
#. change password and username in reveil.recipe

customization
==============
you can change the recipes, remove or add some. if necessary create a .credential file with the same structure as the current one.
