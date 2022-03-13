from selenium.webdriver.common.by import By
import time
import os

from checkAndDownloadFile import checkAndDownloadFile
from findInPortale import findInPortale
from validFileName import validFileName
from applyRenaming import applyRenaming
from log import log

maxTries = 1000

# 	exploreFolder
# 	---------------------------------------------------------------------
# 	Given a parent folder, recursively explores all its subfolders, then
# 	checks the files contained in the parent folder
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- websitePath: the path on the website from the course name
# 			(included) to this folder (included)
# 		- renaming: the renaming dictionary
# 		- portale: the connection to the Portale
# 		- thereIsDropbox: whether the page has a dropbox folder enabled
# 		- downloaded: the list of downloaded files
# 		- ignore: the list of files to be ignored


def exploreFolder(websitePath, renaming, settings, portale, thereIsDropbox, downloaded, ignore):

	# Wait for the table to be correctly loaded
	xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]"
	if findInPortale(portale, xpath, False, False) == None:
		log("ERR", "Could not find material table")
		return

	# Wait some more time in order to be sure that the table to be correctly loaded
	time.sleep(settings["waitTime"])

	# Take the number of folders
	xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding') and not(contains(@class, 'text-warning'))]"
	folders = findInPortale(portale, xpath, True, False)
	if folders != None:
		folders = len(folders)
	else:
		log("ERR", "Could not find folders in the material table")
		return

	# for every folder in the table
	for n in range(folders):
		# Get the folder element, name and path
		for i in range(maxTries):
			folder = portale.find_elements(
				By.XPATH,
				f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding') and not(contains(@class, 'text-warning'))]",
			)
			if len(folder) == folders:
				break
		else:
			log("ERR", "Could not find some folders")
			return

		folder = folder[n]
		folderName = folder.text
		folderPath = os.path.join(websitePath, validFileName(folderName, settings["invalidCharacters"]))

		# Check if folder is desired or not
		replaced = applyRenaming(folderPath, renaming)
		excluded = applyRenaming(replaced, {"other": {}, "regex": dict([(rule, "") for rule in ignore])})

		shouldIgnore = True

		# If the folder is not desired, ignore it
		try:
			if os.path.samefile(excluded, excluded):
				shouldIgnore = False
		except Exception:
			# If error occurred, the excluded is probably an invalid file name, such as a folder name without the final slashes
			# In that case, it should be ignored
			pass

		# If the folder is not undesired, open it and recur
		if not shouldIgnore:

			# Get the clickable link of the folder
			xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding') and not(contains(@class, 'text-warning'))]/../.."
			folderLink = findInPortale(portale, xpath, True, False)
			if folderLink == None:
				log("ERR", f"Could not open folder {folderName}")
				return
			else:
				folderLink = folderLink[n]

			# Double click on it and recur
			portale.execute_script("arguments[0].dispatchEvent(new Event('dblclick'))", folderLink)

			exploreFolder(folderPath, renaming, settings, portale, thereIsDropbox, downloaded, ignore)

			# Every explored folder is being added to the ignored list, so that they are ignored in case of RestartFolder,
			# since they have all been completed already. Using full path in order to be sure to not ignore different
			# subfolders with the same name.
			# When adding a folder, all its subfolders are removed to ease the job of applyRenaming()

			# Remove all the subfolders from the ignored list
			xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding') and not(contains(@class, 'text-warning'))]"
			subfolders = findInPortale(portale, xpath, True, False)
			if subfolders != None:
				for subfolder in subfolders:
					folderPathDoubleBackslash = folderPath.replace("\\", "\\\\")
					if f"{folderPathDoubleBackslash}\\\\{subfolder.text}[\\s\\S]*" in ignore:
						ignore.remove(f"{folderPathDoubleBackslash}\\\\{subfolder.text}[\\s\\S]*")

			# Return to the parent folder
			xpath = "//ol[contains(@class,'breadcrumb')]/li[position() = (last()-2)]/a"
			prevFolder = findInPortale(portale, xpath, False, False)
			if prevFolder != None:
				prevFolder.click()
			else:
				log("ERR", "Could not backtrack on folders")
				return

			# Add the current folder to the ignored list
			folderPathDoubleBackslash = folderPath.replace("\\", "\\\\")
			ignore.append(f"{folderPathDoubleBackslash}[\\s\\S]*")

	# Wait for the table to be correctly loaded again
	time.sleep(settings["waitTime"])

	# Take the number of files
	xpath = f"(//tbody[contains(@class, 'file-item')])[{'2' if thereIsDropbox else '1'}]//tr[not(contains(@class, 'ng-hide'))]//a//span[contains(@class,'ng-binding text-warning') and not(contains(@class, 'videoLezLink'))]"
	files = findInPortale(portale, xpath, True, False)
	if files != None:
		files = len(files)
	else:
		log("ERR", "Could not find files in the folder")
		return

	# for every file in the table, process it with the correct function
	for n in range(files):
		checkAndDownloadFile(
			n, files, portale, thereIsDropbox, settings, renaming, websitePath, downloaded, ignore,
		)

	# Folder has been processed
