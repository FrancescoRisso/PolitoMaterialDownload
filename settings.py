import json
import os

from quitProgram import quitProgram
from log import log

# 	getSettings
# 	---------------------------------------------------------------------
# 	Loads the settings from settings.json and returns it as a dictionary,
# 	if it is considered a valid settings for the program not to crash.
# 	Otherwhise, an error log would be written and the program would quit
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- a dictionary containing all the settings


def getSettings():
	log("INFO", "Loading settings")

	# Load settings
	with open("settings.json", "r") as f:
		d = json.load(f)

	# Check that all the main entries are present and of the correct type
	for key in ["polito", "telegram", "download", "coursesRenaming"]:
		if not key in d:
			quitProgram(None, "Some settings are missing", None)
		if not isinstance(d[key], dict):
			quitProgram(None, "Some settings are invalid", None)

	if not "courses" in d:
		quitProgram(None, "Some settings are missing", None)
	if not isinstance(d["courses"], list):
		quitProgram(None, "Some settings are invalid", None)

	if not "gui" in d:
		quitProgram(None, "Some settings are missing", None)
	if not isinstance(d["gui"], bool):
		quitProgram(None, "Some settings are invalid", None)

	# Check that all the entries for the "polito" key are present and of the correct type
	for key in ["user", "password", "extensionPath"]:
		if not key in d["polito"]:
			quitProgram(None, "Some settings are missing", None)
		if not isinstance(d["polito"][key], str):
			quitProgram(None, "Some settings are invalid", None)

	# Check that all the entries for the "telegram" key are present and of the correct type
	if not "messageType" in d["telegram"]:
		quitProgram(None, "Some settings are missing", None)
	if d["telegram"]["messageType"] not in ["nothing", "error", "recap", "log"]:
		quitProgram(None, "Some settings are invalid", None)

	if d["telegram"]["messageType"] != "nothing":
		for key in ["bot", "chatId"]:
			if not key in d["telegram"]:
				quitProgram(None, "Some settings are missing", None)
			if not isinstance(d["telegram"][key], str):
				quitProgram(None, "Some settings are invalid", None)
	else:
		d["telegram"]["bot"] = ""
		d["telegram"]["chatId"] = ""

	# Check that all the entries for the "download" key are of the correct type
	for rule in d["coursesRenaming"]:
		if not isinstance(rule, str) or not isinstance(d["coursesRenaming"][rule], str):
			quitProgram(None, "Some settings are invalid", None)

	# Check that all the entries for the "download" key are present and of the correct type
	for key in ["mainFolderPath", "ignoreFileName", "renamingFileName"]:
		if key not in d["download"]:
			quitProgram(None, "Some settings are missing", None)
		if not isinstance(d["download"][key], str):
			quitProgram(None, "Some settings are invalid", None)

	for key in ["createEmptyIgnore", "createEmptyRenaming"]:
		if key not in d["download"]:
			quitProgram(None, "Some settings are missing", None)
		if not isinstance(d["download"][key], bool):
			quitProgram(None, "Some settings are invalid", None)

	if "waitTime" not in d["download"]:
		quitProgram(None, "Some settings are missing", None)
	if not isinstance(d["download"]["waitTime"], float):
		quitProgram(None, "Some settings are invalid", None)

	if "invalidCharacters" not in d["download"]:
		quitProgram(None, "Some settings are missing", None)
	if not isinstance(d["download"]["invalidCharacters"], dict):
		quitProgram(None, "Some settings are invalid", None)

	for rule in d["download"]["invalidCharacters"]:
		if not isinstance(d["download"]["invalidCharacters"][rule], str) or not isinstance(rule, str):
			quitProgram(None, "Some settings are invalid", None)

	# Add the download temporary folder path
	d["download"]["tmpDownloadFolder"] = os.path.join(os.getcwd(), "tmpDownload")

	# Return the settings
	return d
