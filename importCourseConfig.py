from yaml import Loader, Dumper, load, dump
import os
import re

from log import log

# 	importCourseConfig
# 	---------------------------------------------------------------------
# 	Imports the renaming dictionary or the ignore list from file
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- path: the path of the course folder
# 		- createIfNotThere: wheter the file should be created if not
# 			present in the folder
# 		- fileName: the name of the file where to read
# 		- isIgnore: whether the function is importing the ignore file. If
# 			false, the function assumes it is importing the renaming dict
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- The renaming dictionary or the ignore list


def importCourseConfig(path, createIfNotThere, fileName, isIgnore):
	# Init the empty renaming dict
	result = [] if isIgnore else {"regex": {}, "other": {}}

	# If the file exists, open it and load it
	if os.path.exists(os.path.join(path, fileName)):
		with open(os.path.join(path, fileName), "r") as f:
			result = load(f, Loader)

			# Check correct formatting
			if isIgnore:
				if not isinstance(result, list):
					return None
			else:
				if (
					not isinstance(result, dict)
					or "regex" not in result
					or "other" not in result
					or not isinstance(result["regex"], dict)
					or not isinstance(result["other"], dict)
				):
					return None

			# Delete any invalid regex expression
			deleteRegex = []
			for expr in result if isIgnore else result["regex"]:
				try:
					re.compile(expr)
				except re.error:
					log("ERR", f"'{expr}' is not a valid regex, will be deleted")
					deleteRegex.append(expr)

			for expr in deleteRegex:
				if isIgnore:
					result.remove(expr)
				else:
					del result["regex"][expr]
	else:
		# If file did not exist, create an empty one if the user requested it
		if createIfNotThere:
			with open(os.path.join(path, fileName), "w") as f:
				dump(result, f, Dumper, default_flow_style=False)

	return result
