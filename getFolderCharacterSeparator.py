import platform


# 	getFolderCharacterSeparator
# 	---------------------------------------------------------------------
# 	Returns the character to separate folder in an operating system
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- regex: whether the character will be inserted in a regex or not
#		- operatingSystem: the desired operating System (leave blank or
# 			set as None for the system os)
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- The correct character according to operating systems rules and
# 			the value of the parameters, if operatingSystem is valid
#		- The name of the os if the parameter operatingSystem is not a
#			recognised parameter, or the system os is not known by the 
# 			program

def getFolderCharacterSeparator(regex: bool, operatingSystem = None):
	if operatingSystem == None:
		operatingSystem = platform.system()

	if operatingSystem == "Windows":
		return "\\\\" if regex else "\\"
	
	if operatingSystem in ["Linux", "Darwin"]:
		return "\\/" if regex else "/"
	
	return operatingSystem
