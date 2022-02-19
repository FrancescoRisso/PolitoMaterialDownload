from selenium.webdriver.common.by import By
import time

maxTries = 600

# 	findInPortale
# 	---------------------------------------------------------------------
# 	Tries to find one/some elements
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- portale: the connection to the Portale della Didattica
# 		- xpath: the xpath to search
# 		- multi: whether the result should be one or a list
# 		- sleep: whether the cycle should wait 0.1s between executions
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- the element, if found
# 		- None if errors occurred


def findInPortale(portale, xpath, multi, sleep):
	for i in range(maxTries):
		try:
			if multi:
				result = portale.find_elements(By.XPATH, xpath)
			else:
				result = portale.find_element_by_xpath(xpath)
			return result
		except Exception:
			if sleep:
				time.sleep(0.05)
	else:
		return None
