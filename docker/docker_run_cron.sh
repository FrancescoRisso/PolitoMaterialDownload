#!/bin/sh

if [ "$cronSettings" = "" ] ; then
	python3 PolitoMaterialDownload.py ;
else
	rm -f /etc/cron.d/crontab;
	echo "${cronSettings} python3 /${workdir}/PolitoMaterialDownload.py \"/${workdir}\" > /proc/1/fd/1 2>&1" >> /etc/cron.d/crontab;
	echo " " >> /etc/cron.d/crontab;
	chmod 0644 /etc/cron.d/crontab
	/usr/bin/crontab /etc/cron.d/crontab;
	echo "Starting cron job";
	cron -f ;
fi
