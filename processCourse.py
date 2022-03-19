import os

from importCourseConfig import importCourseConfig
from restartFolder import RestartFolder
from findInPortale import findInPortale
from exploreFolder import exploreFolder
from log import log


# 	processCourse
# 	---------------------------------------------------------------------
# 	Given a course, opened in a selenium page, downloads any material not
# 	yet in its folder
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- nameFolder: the name of the local course folder (not in the
# 			Portale)
# 		- settings: the download settings
# 		- portale: the selenium connection to the Portale della Didattica
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- a list containing the downloaded files


def processCourse(nameFolder, settings, portale):
	# Compute the folder path
	path = os.path.join(settings["mainFolderPath"], nameFolder)

	# Init the list of downloaded files
	downloaded = []

	# If course folder does not exist, create it
	try:	
		if not os.path.exists(path):
			os.makedirs(path)
	except Exception:
		log("ERR", f"Invalid course folder name: '{nameFolder}'")
		return downloaded

	# Import the renaming dictionary and check if it is correct
	renaming = importCourseConfig(path, settings["createEmptyRenaming"], settings["renamingFileName"], False, settings["os"])
	if renaming == None:
		log("ERR", "Invalid renaming file formatting")
		return downloaded

	# Import the ignore list and check if it is correct
	ignore = importCourseConfig(path, settings["createEmptyIgnore"], settings["ignoreFileName"], True, settings["os"])
	if ignore == None:
		log("ERR", "Invalid ignore file formatting")
		return downloaded

	return downloaded

	# In the course page, select the tab "Materiale"
	xpath = "//a[@class='policorpolink'][normalize-space()='Materiale']"
	materialeTab = findInPortale(portale, xpath, False, True)
	if materialeTab == None:
		log("ERR", "Could not find the tab 'Materiale'")
		return downloaded
	else:
		materialeTab.click()

	# Check if the page has a dropbox folder enabled
	thereIsDropbox = None != findInPortale(portale, "(//a[contains(@href,'#dropboxPanel')])[1]", False, False)

	# Explore the folder until it is all explored, or some errors occurred
	# As explained in restartFolder.py, if a RestartFolder exception occurs, restart exploring the folder
	while True:
		try:
			# Click on the "Materiale didattico" tab
			materialeDidattico = findInPortale(portale, "//a[contains(@href,'#materialiPanel')]", False, False)
			if materialeDidattico == None:
				log("ERR", "Could not find the tab 'Materiale didattico'")
				return downloaded
			else:
				materialeDidattico.click()

			exploreFolder(nameFolder, renaming, settings, portale, thereIsDropbox, downloaded, ignore)
			break
		except RestartFolder:
			continue
		except Exception:
			log("ERR", f"Error while working on '{nameFolder}'")
			return downloaded

	# Return the list of downloaded files
	return downloaded
