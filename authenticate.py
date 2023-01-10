from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from log import log
from quitProgram import quitProgram
from findInPortale import findInPortale
from allMIMEtypes import allMIMEtypes

maxTries = 1000

# 	authenticate
# 	---------------------------------------------------------------------
# 	Connects to the website, and logs in if required
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- settings: the polito settings (<settings.json>.polito)
# 		- tmpFolderPath: the path of the temporary download folder
# 		- gui: whether the user wants the graphic interface or not
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- the connection directly to the portale della didattica


def authenticate(settings, tmpFolderPath, gui):
	# Log connection
	log("INFO", "Connecting to the Portale")

	# Setup all the options
	profile = webdriver.FirefoxProfile()
	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.dir", tmpFolderPath)
	profile.set_preference("browser.helperApps.alwaysAsk.force", False)
	profile.set_preference("browser.download.manager.showWhenStarting", False)
	profile.set_preference("browser.download.manager.showAlertOnComplete", False)
	profile.set_preference("pdfjs.disabled", True)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", allMIMEtypes)
	options = Options()
	if not gui:
		options.headless = True

	# Connect
	try:
		portale = webdriver.Firefox(
			service=Service(GeckoDriverManager(log_level=0).install()), firefox_profile=profile, options=options
		)
	except Exception:
		quitProgram(None, "Could not open Firefox", tmpFolderPath)

	# Install extension
	try:
		portale.install_addon(settings["extensionPath"])
	except Exception:
		quitProgram(portale, "Could not install extension", tmpFolderPath)

	# Go to the Portale della Didattica
	try:
		portale.get("https://didattica.polito.it/")
	except Exception:
		quitProgram(portale, "Could not connect to Portale", tmpFolderPath)

	try:
		# Click login button
		login = findInPortale(portale, "//a[normalize-space()='Login'][1]", False, False)
		if login == None:
			quitProgram(portale, "Could not find login button", tmpFolderPath)
		else:
			login.click()

		# Try to login
		if "Login" in portale.title:
			user = findInPortale(portale, "//input[@id='j_username']", False, False)
			if user == None:
				quitProgram(portale, "Could not find username login field", tmpFolderPath)
			else:
				user.clear()
				user.send_keys(settings["user"])

			pwd = findInPortale(portale, "//input[@id='j_password']", False, False)
			if pwd == None:
				quitProgram(portale, "Could not find password login field", tmpFolderPath)
			else:
				pwd.clear()
				pwd.send_keys(settings["password"])

			loginBtn = findInPortale(portale, "//button[@class='form-element form-button']", False, False)
			if loginBtn == None:
				quitProgram(portale, "Could not find login button", tmpFolderPath)
			else:
				loginBtn.click()
		else:
			# Login not needed
			log("INFO", "Login not required")

		# Wait until page has loaded
		if findInPortale(portale, "//div[@id='titoloPagina'] | //div[@id='table_portali']", False, True) == None:
			quitProgram(portale, "Error while authenticating to the Portale", tmpFolderPath)

		if "Servizi disponibili" in portale.title:
			portaleDellaDidatticaButton = findInPortale(portale, "//div[@id='table_portali']/div/div[normalize-space()='Portale della Didattica']/a", False, False)
			portaleDellaDidatticaButton.click()

	except Exception:
		quitProgram(portale, "Could not login", tmpFolderPath)

	# Wait until page has loaded
	if findInPortale(portale, "//div[@id='titoloPagina']", False, True) == None:
		quitProgram(portale, "Error while authenticating to the Portale", tmpFolderPath)

	# Log whether login is correct
	if portale.title == "Portale della Didattica - Studente":
		log("INFO", "Connected to the Portale")
	else:
		quitProgram(portale, "Error while authenticating to the Portale", tmpFolderPath)

	return portale
