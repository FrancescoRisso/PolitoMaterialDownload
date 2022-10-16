import shutil
import time
import sys
import os

from telegram import initTelegram, telegramLog
from checkNewVersion import checkNewVersion
from log import LOGchangeTelegramConn, log
from findInPortale import findInPortale
from processCourse import processCourse
from authenticate import authenticate
from quitProgram import quitProgram
from importSettings import getSettings


def main():
	# Setup logger for the phase "before connecting to the telegram bot"
	LOGchangeTelegramConn(False)

	# Load the settings
	settings = getSettings(sys.argv)

	if settings["warnNewVersion"]:
		checkNewVersion(sys.argv)

	# Reset the tmpDownload folder
	if os.path.exists(settings["download"]["tmpDownloadFolder"]):
		shutil.rmtree(settings["download"]["tmpDownloadFolder"])
	os.mkdir(settings["download"]["tmpDownloadFolder"])

	# Connect to the bot
	log("INFO", f"Creating bot connection of type '{settings['telegram']['messageType']}'")
	if initTelegram(settings["telegram"]):
		log("INFO", "Bot connected correctly")
	else:
		quitProgram(None, "Error in the bot connection", settings["download"]["tmpDownloadFolder"])

	# Set logger to phase "connected to telegram bot"
	LOGchangeTelegramConn(True)

	# authenticate to the Portale
	portale = authenticate(settings["polito"], settings["download"]["tmpDownloadFolder"], settings["gui"])

	# Get the list of courses with their original and changed names
	courses = {}
	for course in settings["coursesRenaming"]:
		if course in settings["courses"]:
			courses[course] = settings["coursesRenaming"][course]
	for course in settings["courses"]:
		if course not in courses:
			courses[course] = course

	# Setup a dict to store which materials have been saved
	downloadedMaterial = {}

	# Get the list of courses in the Portale
	coursesXpath = '//div[contains(text(), "Carico Didattico A.A.")]/../..//tbody//tr//td//a'
	coursesPortale = findInPortale(portale, coursesXpath, True, False)
	time.sleep(settings["download"]["waitTime"])
	coursesPortale = findInPortale(portale, coursesXpath, True, False)

	if coursesPortale == None:
		quitProgram(portale, "Could not load courses from the Portale", settings["download"]["tmpDownloadFolder"])

	for course in coursesPortale:
		# Only process course if requested in the config file
		courseName = course.text
		if courseName in courses:

			# Log
			log("SAVE", f"Checking material from course '{os.path.basename(courses[courseName])}'")

			# Open course page in a new tab
			portale.execute_script(f"window.open(\"{course.get_attribute('href')}\", '_blank');")
			portale.switch_to.window(portale.window_handles[1])

			# Process the course and update the downloaded material list
			downloadedMaterial[courses[courseName]] = processCourse(courses[courseName], settings["download"], portale)
			if downloadedMaterial[courses[courseName]] == []:
				del downloadedMaterial[courses[courseName]]

			# Close the tab
			portale.close()
			portale.switch_to.window(portale.window_handles[0])

			# Remove the course from the list of courses
			del courses[courseName]

	# If some courses have not been processed, log an error
	for course in courses:
		log("ERR", f"'{course}' not found")

	# Log download recap
	try:
		if len(downloadedMaterial.keys()) == 0:
			telegramLog("\nNo files downloaded\n", "")
		else:
			telegramLog("\nDownloaded files:", "")
			for course in downloadedMaterial:
				telegramLog(f"- {course}", "")
				for file in downloadedMaterial[course]:
					telegramLog(f"  - {file}", "")
	except Exception:
		log("ERR", "Bot is not connected")

	# All done, quit
	quitProgram(portale, "", settings["download"]["tmpDownloadFolder"])


if __name__ == "__main__":
	main()
