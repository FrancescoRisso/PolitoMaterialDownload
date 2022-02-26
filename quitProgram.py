import shutil
import time
import sys
import os

from telegram import telegramSendMessage
from log import log

waitBeforeQuitting = True


# 	setWaitBeforeQuitting
# 	---------------------------------------------------------------------
# 	Sets a value for the setting waitBeforeQuitting
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- val: the boolean value it should be set to


def setWaitBeforeQuitting(val):
	global waitBeforeQuitting
	waitBeforeQuitting = val


# 	quitProgram
# 	---------------------------------------------------------------------
# 	Closes all the opened "things", sends the telegram log and quits the
# 	program
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- portale: the selenium connection to be closed (None if it is
# 			not opened)
# 		- error: the error message to be logged ("" if clean exit)


def quitProgram(portale, error, tmpDownload):
	# If there is an error, log it
	if error != "":
		log("ERR", error)

	# If the connection to the Portale is opened, close it
	if portale != None:
		portale.quit()

	# Send message and log it
	log("INFO", "Sending Telegram report")
	try:
		telegramSendMessage()
	except Exception:
		log("ERR", "Could not send Telegram message")

	# If there is a temporary download folder, remove it
	if tmpDownload != None and os.path.exists(tmpDownload):
		shutil.rmtree(tmpDownload)

	time.sleep(0.2)

	try:
		if os.path.exists(os.path.join(os.getcwd(), "geckodriver.log")):
			os.remove(os.path.join(os.getcwd(), "geckodriver.log"))
	except Exception:
		pass

	if waitBeforeQuitting:
		input(f"{'The execution has finished.' if error=='' else 'Quitting due to an error.'} Press enter to quit.")

	# Quit the program
	sys.exit()
