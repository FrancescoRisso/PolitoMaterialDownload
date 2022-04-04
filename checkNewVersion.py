from urllib.request import urlopen

from log import log


def checkNewVersion():
	# Retreive current version from CHANGELOG.md file
	try:
		f = open("CHANGELOG.md", "r")
	except:
		log("ERR", "Could not open CHANGELOG.md to verify version")
		return

	for line in f:
		if "Version" in line:
			thisVersion = line
			break
	else:
		log("ERR", "Could not retrieve current version")
		return

	f.close()

	thisVersion = str(thisVersion).replace("##", "").replace("Version", "").strip()

	# Retreive latest github version
	lastVersion = urlopen(
		"https://raw.githubusercontent.com/FrancescoRisso/PolitoMaterialDownload/main/CHANGELOG.md"
	).read(50)
	lastVersion = str(lastVersion).split("##")[1].strip().split("\\n")[0].replace("Version", "").strip()

	if lastVersion != thisVersion:
		log("ERR", f"A new version is available: {lastVersion} (Your version: {thisVersion})")  # TODO
	else:
		log("INFO", f"Version {thisVersion} (installed) is the latest")
