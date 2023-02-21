import platform
from yaml import Loader, load
import os

from quitProgram import setWaitBeforeQuitting
from quitProgram import quitProgram
from log import log

# 	getSettings
# 	---------------------------------------------------------------------
# 	Loads the settings from settings.json and returns it as a dictionary,
# 	if it is considered a valid settings for the program not to crash.
# 	Otherwhise, an error log would be written and the program would quit
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- argv: the argv received by the main
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- a dictionary containing all the settings


def getSettings(argv):

	try:
		# Load settings
		with open(os.path.join(argv[1] if len(argv) > 1 else os.getcwd(), "settings.yaml"), "r", encoding="utf-8") as f:
			d = load(f, Loader)
	except Exception:
		quitProgram(None, "Unable to open the settings configuration", None)

	# Check if waitBeforeQuitting is ok, and if so update the quitter
	if "waitBeforeQuitting" in d:
		if isinstance(d["waitBeforeQuitting"], bool):
			setWaitBeforeQuitting(d["waitBeforeQuitting"])
		else:
			quitProgram(None, "Setting 'waitBeforeQuitting' is incorrect", None)
	else:
		quitProgram(None, "Setting 'waitBeforeQuitting' is missing", None)

	# Log
	log("INFO", "Loading settings")

	# Get info about the operating system
	operatingSystem = platform.system()

	# Check that all the main entries are present and of the correct type
	for key in ["polito", "telegram", "download", "coursesRenaming"]:
		if not key in d:
			quitProgram(None, f"Setting '{key}' is missing", None)
		if not isinstance(d[key], dict):
			quitProgram(None, f"Setting '{key}' is incorrect", None)

	if not "courses" in d:
		quitProgram(None, f"Setting 'courses' is missing", None)
	if not isinstance(d["courses"], list):
		quitProgram(None, f"Setting 'courses' is incorrect", None)

	for key in ["gui", "warnNewVersion"]:
		if not key in d:
			quitProgram(None, f"Setting '{key}' is missing", None)
		if not isinstance(d["gui"], bool):
			quitProgram(None, f"Setting '{key}' is incorrect", None)

	# Check that all the entries for the "polito" key are present and of the correct type
	for key in ["user", "password"]:
		if not key in d["polito"]:
			quitProgram(None, f"Setting 'polito/{key}' is missing", None)
		if not isinstance(d["polito"][key], str):
			quitProgram(None, f"Setting 'polito/{key}' is incorrect", None)

	# Check that all the entries for the "telegram" key are present and of the correct type
	if not "messageType" in d["telegram"]:
		quitProgram(None, f"Setting 'telegram/messageType' is missing", None)
	if d["telegram"]["messageType"] not in ["nothing", "error", "recap", "log"]:
		quitProgram(None, f"Setting 'telegram/messageType' is incorrect", None)

	if d["telegram"]["messageType"] != "nothing":
		for key in ["bot", "chatId"]:
			if not key in d["telegram"]:
				quitProgram(None, f"Setting 'telegram/{key}' is missing", None)
			if not isinstance(d["telegram"][key], str):
				quitProgram(None, f"Setting 'telegram/{key}' is incorrect", None)
	else:
		d["telegram"]["bot"] = ""
		d["telegram"]["chatId"] = ""

	# Check that all the entries for the "coursesRenaming" key are of the correct type
	for rule in d["coursesRenaming"]:
		if not isinstance(rule, str) or not isinstance(d["coursesRenaming"][rule], str):
			quitProgram(None, f"Setting 'coursesRenaming/{key}' is incorrect", None)

	# Check that all the entries for the "download" key are present and of the correct type
	for key in ["mainFolderPath", "ignoreFileName", "renamingFileName"]:
		if key not in d["download"]:
			quitProgram(None, f"Setting 'download/{key}' is missing", None)
		if not isinstance(d["download"][key], str):
			quitProgram(None, f"Setting 'download/{key}' is incorrect", None)

	for key in ["createEmptyIgnore", "createEmptyRenaming", "deleteReplaced"]:
		if key not in d["download"]:
			quitProgram(None, f"Setting 'download/{key}' is missing", None)
		if not isinstance(d["download"][key], bool):
			quitProgram(None, f"Setting 'download/{key}' is incorrect", None)

	if "waitTime" not in d["download"]:
		quitProgram(None, f"Setting 'download/waitTime' is missing", None)
	if not isinstance(d["download"]["waitTime"], float) and not isinstance(d["download"]["waitTime"], int):
		quitProgram(None, f"Setting 'download/waitTime' is incorrect", None)

	if "invalidCharacters" not in d["download"]:
		quitProgram(None, f"Setting 'download/invalidCharacters' is missing", None)
	if not isinstance(d["download"]["invalidCharacters"], dict):
		quitProgram(None, f"Setting 'download/invalidCharacters' is incorrect", None)

	for rule in d["download"]["invalidCharacters"]:
		if not isinstance(d["download"]["invalidCharacters"][rule], str) or not isinstance(rule, str):
			quitProgram(None, f"Setting 'download/invaildCharacters/{rule}' is incorrect", None)

	# if not deleteReplaced, check that the moveDest is present and of the correct type
	if not d["download"]["deleteReplaced"]:
		if not "moveDest" in d["download"]:
			quitProgram(None, f"Setting 'download/moveDest' is missing", None)
		if not isinstance(d["download"]["moveDest"], str):
			quitProgram(None, f"Setting 'download/moveDest' is incorrect", None)
	else:
		d["download"]["moveDest"] = ""

	if operatingSystem == "Windows":
		d["download"]["mainFolderPath"] = d["download"]["mainFolderPath"].replace("/", "\\")
		d["download"]["moveDest"] = d["download"]["moveDest"].replace("/", "\\")
	elif operatingSystem in ["Linux", "Darwin"]:
		d["download"]["mainFolderPath"] = d["download"]["mainFolderPath"].replace("\\", "/")
		d["download"]["moveDest"] = d["download"]["moveDest"].replace("\\", "/")
	else:
		quitProgram(None, f"Your operating system ({operatingSystem}) is not recognised", None)

	d["download"]["os"] = operatingSystem

	# Check that the ignore and rename file names are yaml file names
	for key in ["ignoreFileName", "renamingFileName"]:
		if not d["download"][key].endswith(".yaml"):
			quitProgram(None, f"Setting 'download/{key}' is incorrect", None)

	# Add the download temporary folder path and the polito.it extension path
	d["download"]["tmpDownloadFolder"] = os.path.join(os.getcwd(), "tmpDownload")
	d["polito"]["extensionPath"] = os.path.join(argv[1] if len(argv) > 1 else os.getcwd(), "politoit_utility.xpi")

	# Return the settings
	return d
