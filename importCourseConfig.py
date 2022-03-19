from yaml import Loader, Dumper, load, dump
import platform
import os
import re

from log import log
from quitProgram import quitProgram

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


def importCourseConfig(path, createIfNotThere, fileName, isIgnore, operatingSystem):
	# Init the empty renaming dicts (result is the original one, r is the one with updated slashes)
	result = {"regex": [] if isIgnore else {}, "other": [] if isIgnore else {}}
	r = {"regex": [] if isIgnore else {}, "other": [] if isIgnore else {}}

	# If the file exists, open it and load it
	if os.path.exists(os.path.join(path, fileName)):
		with open(os.path.join(path, fileName), "r", encoding="utf-8") as f:
			result = load(f, Loader)

			# Check correct formatting
			if (
				not isinstance(result, dict)
				or "regex" not in result
				or "other" not in result
				or not isinstance(result["regex"], list if isIgnore else dict)
				or not isinstance(result["other"], list if isIgnore else dict)
			):
				return None

			if isIgnore:
				d = {}
				for rule in result["regex"]:
					d[rule] = ""
				result["regex"] = d
				d = {}
				for rule in result["other"]:
					d[rule] = ""
				result["other"] = d

			# Delete any invalid regex expression
			deleteRegex = []
			for expr in result["regex"]:
				try:
					re.compile(expr)
				except re.error:
					log("ERR", f"'{expr}' is not a valid regex, will be deleted")
					deleteRegex.append(expr)

			for expr in deleteRegex:
				if isIgnore:
					result["regex"].remove(expr)
				else:
					del result["regex"][expr]
	else:
		# If file did not exist, create an empty one if the user requested it
		if createIfNotThere:
			with open(os.path.join(path, fileName), "w") as f:
				dump(result, f, Dumper, default_flow_style=False)

	if isIgnore:
		if operatingSystem == "Windows":
			for key in result["regex"]:
				r["regex"].append(key.replace("\\/", "\\\\"))
			for key in result["other"]:
				r["other"].append(key.replace("/", "\\"))

		elif operatingSystem in ["Linux", "Darwin"]:
			for key in result["regex"]:
				r["regex"].append(key.replace("\\\\", "\\/"))
			for key in result["other"]:
				r["other"].append(key.replace("\\", "/"))
	else:
		if operatingSystem == "Windows":
			for key in result["regex"]:
				r["regex"][key.replace("\\/", "\\\\")] = result["regex"][key].replace("\\/", "\\\\")
			for key in result["other"]:
				r["other"][key.replace("/", "\\")] = result["other"][key].replace("/", "\\")

		elif operatingSystem in ["Linux", "Darwin"]:
			for key in result["regex"]:
				r["regex"][key.replace("\\\\", "\\/")] = result["regex"][key].replace("\\\\", "\\/")
			for key in result["other"]:
				r["other"][key.replace("\\", "/")] = result["other"][key].replace("\\", "/")

	return r
