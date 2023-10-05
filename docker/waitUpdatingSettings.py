import os
import time
import urllib.request

open("./onedrive_settings/login_link", "a").close()

FNAME = "./remove_me"
onedriveFile = "./onedrive_settings/default-config"
pmdFile = "./polito_material_download_settings/sample-settings.yaml"

open(FNAME, "w").close()

print(
	f"""
Operate the changes to the settings, then delete the file '{FNAME}'
\t- Edit '/polito_material_download_settings/settings.yaml' to your will
\t\tYou have a default one as 'sample-settings.yaml'
\t\t! Please do not change the mainFolderPath setting
\t\t! Please leave gui and waitBeforeQuitting to 'No' to avoid errors
\t\t! If you have the moveDest setting, it should be a subfolder of mainFolderPath to be synced
\t- Edit '/onedrive_settings/config' to your will
\t\tYou have a default one as 'default-config'
\t\t! Please do not change the sync_dir option
\t\tIf this is the first run of the onedrive container, write the login link into '/onedrive_settings/login_link'""",
	flush=True,
)

if not os.path.exists(pmdFile):
	# Download PMD sample-settings.yaml file
	urllib.request.urlretrieve(
		"https://raw.githubusercontent.com/FrancescoRisso/PolitoMaterialDownload/main/settings/sample-settings.yaml", pmdFile,
	)

	# Prepare the mainFolderPath value
	f = open(pmdFile, "r")
	content = f.read()
	f.close()
	f = open(pmdFile, "w")
	f.write(
		content.replace(
			' mainFolderPath: "C:\\\\Users\\\\user\\\\Polito\\\\Corsi"', ' mainFolderPath: "/PolitoMaterialDownload/data"'
		).replace("waitBeforeQuitting: Yes", "waitBeforeQuitting: No")
	)
	f.close()

if not os.path.exists(onedriveFile):
	# Download onedrive default-config file
	urllib.request.urlretrieve("https://raw.githubusercontent.com/abraunegg/onedrive/master/config", onedriveFile)

	# Prepare the sync_dir value
	f = open(onedriveFile, "r")
	content = f.read()
	f.close()
	f = open(onedriveFile, "w")
	f.write(content.replace('# sync_dir = "~/OneDrive"', 'sync_dir = "/onedrive/data"'))
	f.close()


for i in range(60 * 10):  # Leave a maximum of 10 mins
	if not os.path.exists(FNAME):
		print("Settings updated, the settings container will now quit")
		break

	time.sleep(1)
else:
	print("Settings not updated, aborting the settings container execution")
	os.remove(FNAME)
