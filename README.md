# PolitoMaterialDownload

## Introduction

This is a tool for students from the Politecnico di Torino, to help them downloading the materials uploaded by the professors on the Portale della Didattica.

You give this tool your Portale della Didattica credentials, a folder and the list of courses you want: it will check, for the courses you asked, which files from the Portale are not there in the folder, and it will download them.

The folder can be either local, or on a cloud service like Dropbox or Onedrive. In this second case, you can also use an always on server, and set it up so that this script is executed periodically.

You can also set this toool so that some files or folders are ignored or renamed, allowing you to not be forced to use the same file names as uploaded by the professors.

A file from the Portale will be downloaded if there isn't any file with _the same name\*_ in the corresponding local folder, or if the file is present, but its last modified date is before the updload date on the Portale (so your local file is outdated).

\* As explained above, you can set some rules to change a certain name on the Portale to another name in the local folder (more details in [SETTINGS.md](SETTINGS.md)).

## Execution time disclaimer

This tool is quite slow to execute: this is because the software emulates a real user interacting with a browser (Firefox) and the elements in the Portale, thus needing some time to be sure that the elements have correctly loaded in the page (which is sometimes a relatively long time).

I tested the tool with the course "Analisi Matematica II", at the end of the semester (so there were a lot of files). It took about 20 mins to process the course when it had to download all the files, while it took around 1 min when all the files were already up to date.

Of course, downloading the files manually would take less time globally, but it would take you more time. I see this tool as I see a robot cleaner: cleaning the room by yourself might take you 10 mins, while the robot might take more than 1 hour. The advantage is that the robot will take you only a couple of seconds, the time to press a button.

Here is the same: downloading the files manually would take less time, but what's the matter if the script does run for longer, if you can do other things in the meantime, and you just have to launch it? Or you even set it up to launch regularly by itself?

## Test disclaimer

I have developed and "lab-tested" this tool, but as now (february 2022) I havent't really used it on a daily basis.

This might mean that there are still strange problems not picked up by the lab-testing, if you find some please report them. I will be using this tool for the next semester and will be fixing any bug that I find.

## Updating

I will be using this tool, so I might find and fix new bugs, or I might add new useful features. Every update will be published here, and the changes will be tracked in the file [CHANGELOG.md](CHANGELOG.md).

When updating to a new version, please give a look to the changelog's versions from the one you are updating from to the current version: you might need to add/modify some settings. If you have to change something, it will be marked as `NOTE` in the changelog.

You can also have the program check for you if there are available updates, see [SETTINGS.md](SETTINGS.md) for details.

## How to install

-   Download all the code to your machine (either with `git clone` or by downloading the zip folder, then exctracting).

-   In the same directory of the code, create a `settings.yaml` file as explained in [SETTINGS.md](SETTINGS.md).

-   If you don't have python, install it (I have not tested the tool with python v2, but with python v3 it works).

-   If you don't have pip, install it.

-   Install the required python modules entering the following command in a terminal: `pip install -r requirements.txt` (replace `pip` with `pip3` if you are on linux and you use python 3).

-   If you don't have mozilla Firefox, install it.

-   Run the program by launching the file `PolitoMaterialDownload.py`.

## Automating it

I have an Ubuntu always on server, and I save my Polito files on a Dropbox folder. For these reasons, I could use that server to automate the execution of this program, and get the files uploaded directly to my Dropbox (thus, finding them on my PC).

Here are the steps I followed:

- Installed dropbox, following partially [this guide](https://www.fosslinux.com/45045/headless-dropbox-ubuntu-server.htm) (Not the best guide, but it is what I found: I had to remove the file it told me to create in `\etc\init.d`, and I had to change the service config).
My service config is:
	```
	[Unit]
	Description=Dropbox Daemon
	After=network.target

	[Service]
	ExecStart=/bin/sh -c '/opt/dropbox/dropboxd start'
	ExecStop=/bin/sh -c '/opt/dropbox/dropboxd stop'
	PIDFile=${HOME}/.dropbox/dropbox.pid
	User=downloader
	Group=downloader
	Type=forking
	Restart=on-failure
	RestartSec=5
	StartLimitInterval=60s
	StartLimitBurst=3

	[Install]
	WantedBy=multi-user.target
	```
	If you install Dropbox too, from this file change User and Group to your server username, and change the path in ExecStart and ExecStop.

- Downloaded the code via `git clone`.

- Configured the settings file (a useful command was `readlink -f <file>` to get the absolute path to a file or a directory).

- Run the program manually once via the command `python3 PolitoMaterialDownload.py`. I higly recommend doing this to check that all settings are ok, since every error before the loading of the setting `waitBeforeQuitting` would require user interaction to quit (and this would make the program hang forever). If you checked that the settings were correct, this problem should not happen anymore.

- There was a warning:
	```
	/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.8) or chardet (3.0.4) doesn't match a supported version!
	```
	I solved it by executing `pip3 install --upgrade requests`.

- Created using `mkdir` and `touch` a file for logging and a file for errors (I did it inside `\var\log`).

- Executed the command `sudo chmod a+w FILE` on both the logging and error files.

- Scheduled the script to be executed every hour, by editing crontab file (via the command `crontab -e`), inserting the following line:
	```
	0 * * * * python3 /home/downloader/PolitoMaterialDownload/PolitoMaterialDownload.py "/home/downloader/PolitoMaterialDownload" 1>> /var/log/downloader/log.log 2>> /var/log/downloader/error.log
	```
	If you want to schedule the script too, you should replace:
	- the `0 * * * *` with a valid cron setting of your choice (this one is "every hour").
	- `/home/downloader/PolitoMaterialDownload/PolitoMaterialDownload.py` with the full path to the file `PolitoMaterialDownload.py`.
	- `"/home/downloader/PolitoMaterialDownload"` with the full path to the folder where the code is (please enclose it in double quotes as I did).
	- `/var/log/downloader/log.log` with the path to the file where you want your main log to be stored.
	- `/var/log/downloader/error.log` with the path to the file where you want your error log to be stored (can also be the same as above).<br>
		Please note that all "ERR" logs would still be sent to the first file: this is only in case the program crashes in a very strange way.

## Ignoring or renaming files or folders

It is possible to set this tool to ignore or rename certains files or folders.

Please refer to the [SETTINGS.md](SETTINGS.md) file for more details.

## Possible error messages

[ERRORS.md](ERRORS.md) contains the list of all the possible error messages of the program, including more information about the error, the possible reason, what does the program do when encounters that problem (quit, ignore the file, ignore the folder...) and what I suggest you to do when it happens.

## Telegram integration

This program allows you to receive Telegram notification about the status of every execution of the software.

This is especially useful if you are not running the software on your machine (for example, you run the code on an always-on server, that regularly runs the code for you).

In order to receive telegram updates, you need to own a Telegram bot: unfortunately for security reasons we cannot use a single one (this would mean to share the bot token, which is highly discouraged, since everyone that has that token can do anything they want with the bot).

Since not everyone might want to create a bot, and not everyone might need it, you can disable the Telegram feature (see [SETTINGS.md](SETTINGS.md) for details).

If you already own a Telegram bot, I have good news for you: since this tool does only push messages to Telegram (no messages from user to bot are implemented), it does not need any infinity polling, so you can re-use an existing bot even if you have it running somewhere else.

If you do not own a Telegram bot, creating it is simple: in the Telegram app, start a chat with [@BotFather](https://t.me/botfather), send the `/newbot` command, give a name and a tag to your bot and you're done, you just have to copy the token that [@BotFather](https://t.me/botfather) gives you

## Important notes

- The software uses a temporary download folder, which is a folder called `tmpDownload` inside the folder where the code is. This folder is emptied and deleted every time the program runs, so please be advised that if you manually create a folder with that name, and store some files inside, they would be deleted. 

- If you launch the program from a folder that is not the code folder, you should launch it with an extra parameter, which is the location of the code folder (as what I did in the crontab settings in the section "Automating it").

- I have tested this program on Windows and Linux, but I could not try it on macOS. On Windows it worked perfectly to me, while on Linux I encountered this warning:
	```
	/usr/lib/python3/dist-packages/requests/__init__.py:89: RequestsDependencyWarning: urllib3 (1.26.8) or chardet (3.0.4) doesn't match a supported version!
	```
	It does not really affect the program, but if you find it annoying you can fix it via the command `pip3 install --upgrade requests` to fix it.
