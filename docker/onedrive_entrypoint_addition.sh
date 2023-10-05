link_file="/onedrive/conf/login_link"

if [ "${QUIT_AFTER_LINK:=0}" == "1" ]; then
	link_file="temporary_file"
	echo "." > $link_file
fi

echo "# Launching onedrive"
# Only switch user if not running as target uid (ie. Docker)
if [ "$ONEDRIVE_UID" = "$(id -u)" ]; then
   /usr/local/bin/onedrive "${ARGS[@]}" < $link_file
else
   chown "${oduser}:${odgroup}" /onedrive/data /onedrive/conf
   exec gosu "${oduser}" /usr/local/bin/onedrive "${ARGS[@]}" < $link_file
fi
