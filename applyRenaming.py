import re

# 	applyRenaming
# 	---------------------------------------------------------------------
# 	Given a string and some replacing rules, returns the string with all
# 	the replacing done
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- string: the string where to replace
# 		- renaming: the dict of rules
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- the updated string


def applyRenaming(string, renaming):
	for rule in renaming["other"]:
		string = string.replace(rule, renaming["other"][rule])
	for rule in renaming["regex"]:
		string = re.sub(rule, renaming["regex"][rule], string)
	return string
