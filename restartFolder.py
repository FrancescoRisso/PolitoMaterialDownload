# A custom exception
# There is a bug in the Portale, such that sometimes doing a download
# would redirec you to the file itself. Going back in history will bring
# you back to the correct page, but at root folder. For this reason,
# when I encounter this issue I have to explore again all the folder, in
# order to be sure to check all files.
# I use this exception to differenciate when this problem happens from
# when another error happens: if the problem explained above occurs, I
# want to explore again the folder; if another problem occurs I want to
# log it and skip the rest of the files in the course


class RestartFolder(Exception):
	pass
