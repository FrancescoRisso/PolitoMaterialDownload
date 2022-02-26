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

## How to install

-   Download all the code to your machine (either with `git clone` or by downloading the zip folder, then exctracting).

-   In the same directory of the code, create a `settings.yaml` file as explained in [SETTINGS.md](SETTINGS.md).

-   If you don't have python, install it (I have not tested the tool with python v2, but with python v3 it works).

-   If you don't have pip, install it.

-   Install the required python modules entering the following command in a terminal: `pip install -r requirements.txt` (replace `pip` with `pip3` if you are on linux and you use python 3).

-   If you don't have mozilla Firefox, install it.

-   Run the program by launching the file `PolitoMaterialDownload.py`.

## Automating it

_Work in progress_

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

## Important note

The software uses a temporary download folder, which is a folder called `tmpDownload` inside the folder where the code is. This folder is emptied and deleted every time the program runs, so please be advised that if you manually create a folder with that name, and store some files inside, they would be deleted. 


