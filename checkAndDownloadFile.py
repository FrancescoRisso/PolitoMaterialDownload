from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os
import shutil

from restartFolder import RestartFolder
from findInPortale import findInPortale
from validFileName import validFileName
from applyRenaming import applyRenaming
from log import log

maxTries = 1000

# 	checkAndDownloadFile
# 	---------------------------------------------------------------------
# 	Given a file, checks if it should be downloaded, and downloads it if
# 	required
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- n: the 0-based number of the file in the current working folder
# 		- filesNumber: the number of files in the current working folder
# 		- portale: the selenium connection to the Portale della Didattica
# 		- thereIsDropbox: whether this course has the Dropbox tab
# 		- settings: the download settings
# 		- renaming: the dictionary of renaming rules
# 		- folderPathOnWebsite: the path of the current working folder in
# 			the browser (so not corrected using renaming)
# 		- downloaded: the list of the downloaded files
# 		- ignore: the list of things to be ignored
# 	---------------------------------------------------------------------
# 	OUPTUT:
# 		- 0 if all went smoothly
# 		- -1 if the download opened the bugged page, so the exploration
# 			of the folders should restart from the root


def checkAndDownloadFile(
	n, filesNumber, portale, thereIsDropbox, settings, renaming, folderPathOnWebsite, downloaded, ignore,
):
	restart = False

	# Get the file element and name
	for i in range(maxTries):
		files = portale.find_elements(
			By.XPATH,
			f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding text-warning')]",
		)
		if len(files) == filesNumber:
			break
	else:
		log("ERR", "Could not find some files")
		return

	file = files[n]
	fileName = file.text

	# If the displayed file name has been truncated (ends with ...), take it from its link's title (see the html of the Portale)
	if fileName.endswith("..."):
		xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding text-warning')]/.."
		file = findInPortale(portale, xpath, True, False)
		if file == None:
			log("ERR", f"Could not find complete name for '{fileName}'")
			return
		else:
			fileName = file[n].get_attribute("title")
		fileName = fileName[: fileName.rfind(".") - 1]
		fileName = fileName[: fileName.rfind(" ")]

	# Remove characters that cannot be in a file name
	fileName = validFileName(fileName, settings["invalidCharacters"])

	# Compute the file's path in the folder (path relative to the main folder, where all the courses folders are)
	filePathInFolder = applyRenaming(os.path.join(folderPathOnWebsite, fileName), renaming)
	excluded = applyRenaming(filePathInFolder, ignore)

	if filePathInFolder != excluded:
		return

	# Take the date of the updload of the file to the server
	xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding text-warning')]/../../../td[4]"
	server_lastModified = findInPortale(portale, xpath, True, False)
	if server_lastModified == None:
		log("ERR", f"Could not find upload date for '{fileName}'")
		return
	else:
		server_lastModified = datetime.strptime(server_lastModified[n].text.strip(), "%d/%m/%Y %H:%M:%S")

	# Compute the folder's absolute path, and create it if it does not exist
	completeFolderPath = os.path.join(settings["mainFolderPath"], os.path.dirname(filePathInFolder))
	if not os.path.exists(completeFolderPath):
		os.makedirs(completeFolderPath)

	# Compute the file's absolute path
	completeFilePath = os.path.join(settings["mainFolderPath"], filePathInFolder)

	# If the file does not exist in the local folder, or it is outdated, download it
	if (
		not os.path.exists(completeFilePath)
		or datetime.fromtimestamp(os.path.getmtime(completeFilePath)) < server_lastModified
	):

		# Click the download button
		xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding text-warning')]/../../../td[1]/a[1]"
		download = findInPortale(portale, xpath, True, False)
		if download == None:
			log("ERR", f"Could not find download button for '{fileName}'")
			return
		else:
			download[n].click()
			time.sleep(settings["waitTime"])

		# If page changed (see at the beginning of the file), go back in page history and, after saving this file, restart exploring the folder
		if portale.title == "" or "idp.polito" in portale.title:
			portale.execute_script("window.history.go(-1)")
			restart = True

		# Wait to be sure the download has started
		time.sleep(settings["waitTime"])

		# Try to process until the download is complete or failed
		while len(os.listdir(settings["tmpDownloadFolder"])) != 0:

			# Compute the absolute file path of the downloaded file (in the tmpDonwload folder)
			finalFileName = os.path.join(settings["tmpDownloadFolder"], sorted(os.listdir(settings["tmpDownloadFolder"]))[-1])

			# If download is complete, move it to the correct location, then stop checking
			if not finalFileName.endswith(".part") and len(os.listdir(settings["tmpDownloadFolder"])) == 1:

				# If there is an outdated file
				if os.path.exists(completeFilePath):

					# If the user wants it to be deleted, delete it
					if settings["deleteReplaced"]:
						os.remove(completeFilePath)

					# If the user wants it to be moved, move it
					else:
						# Create folder if not present
						if not os.path.exists(settings["moveDest"]):
							os.mkdir(settings["moveDest"])

						shutil.move(
							completeFilePath, os.path.join(settings["moveDest"], f"{time.time()} {os.path.basename(completeFilePath)}")
						)
						# Wait until file has been moved
						for i in range(1200):
							if os.path.basename(completeFilePath) not in os.listdir(settings["moveDest"]):
								break
							time.sleep(0.05)
						else:
							os.remove(finalFileName)
							log("ERR", f"Could not move '{os.path.basename(completeFilePath)}' to the 'moveDest' folder. Skipping it")
							return

					log("SAVE", f"Replacing '{os.path.basename(completeFilePath)}'")
					downloaded.append(f"{os.path.basename(completeFilePath)} (replaced)")
				else:
					log("SAVE", f"Saving '{os.path.basename(completeFilePath)}'")
					downloaded.append(os.path.basename(completeFilePath))

				# Move the downloaded file to the correct location (and rename it)
				shutil.move(finalFileName, completeFilePath)

				# Wait until the folder is totally empty
				for i in range(1200):
					if len(os.listdir(settings["tmpDownloadFolder"])) == 0:
						break
					time.sleep(0.05)
				else:
					log("ERR", f"Could not move '{os.path.basename(completeFilePath)}' to the correct folder. Deleting it")
					for file in os.listdir(settings["tmpDownloadFolder"]):
						os.remove(os.path.join(settings["tmpDownloadFolder"], file))
					
					# Remove non-moved file if exists (can be a 0-bytes file)
					if os.path.exists(completeFilePath):
						os.remove(completeFilePath)

					# Remove file from downloaded list
					downloaded.pop()

				break

			# Else, wait some more time
			time.sleep(0.5)
		else:
			# If while interrupted because folder was empty, download has failed
			log("ERR", f"Could not download '{fileName}'")

	if restart:
		raise RestartFolder()
