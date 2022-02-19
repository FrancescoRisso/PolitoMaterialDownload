# 	validFileName
# 	---------------------------------------------------------------------
# 	Given a string, replaces all the characters that cannot be in the
# 	name of a file or a directory
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- string: the string to operate with
# 		- instructions: a dict that pairs the invalid character with what
# 			it should be replaced with
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- the updated string


def validFileName(string, pairings):
	for char in pairings:
		string = string.replace(char, pairings[char])
	return string.strip()
