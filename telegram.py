import telebot

chatId = None
msgType = None
finalMessage = ""
conn = None
initExecuted = False

# 	initTelegram
# 	---------------------------------------------------------------------
# 	Setup a chat with a telegram bot
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- settings: a dictionary containing the settings for the bot
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- whether the init was successful or not


def initTelegram(settings):
	global initExecuted
	global chatId
	global msgType
	global finalMessage
	global conn

	# Store the settings
	msgType = settings["messageType"]
	finalMessage = ""
	initExecuted = True

	# Try to create the connection item
	try:
		if msgType != "nothing":
			conn = telebot.TeleBot(settings["bot"])
			chatId = settings["chatId"]
		else:
			conn = None
		return True
	except Exception:
		initExecuted = False
		return False


# 	telegramLog
# 	---------------------------------------------------------------------
# 	If required from msgType, stores some text to the final message
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- newMessageToInsert: the text to be stored (if required)
# 		- type: the type of log message (INFO, SAVE, ERR, "" if not
# 			coming from the log function)


def telegramLog(newMessageToInsert, type):
	global finalMessage
	global initExecuted

	# Check that bot is correctly set up
	if not initExecuted:
		raise Exception("Please execute initTelegram before using telegramLog")

	# Do nothing if the new message is empty, or the user requested no messages
	if newMessageToInsert == "" or msgType == "nothing":
		return

	# Do not start the final message with a \n
	if finalMessage == "" and newMessageToInsert.startswith("\n"):
		newMessageToInsert = newMessageToInsert[1:]

	# Append the new message to the final message if the user requested the whole log,
	# or if the message is an error or does not come from log (type=="")
	if msgType == "log" or type == "ERR" or (type == "" and msgType != "error"):
		middleChar = '' if len(finalMessage) == 0 else '\n'
		finalMessage = f"{finalMessage}{middleChar}{newMessageToInsert}"
		return


# 	splitText
# 	---------------------------------------------------------------------
# 	Splits a text in grups of max 4999 chars, while avoiding splitting
# 	in the middle of a message
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- text: the message to be split
# 	---------------------------------------------------------------------
# 	OUTPUT:
# 		- a list of strings, containing the splitted message


def splitText(text):
	splitted = []
	if len(text) > 4000:
		index = text[:4000].rfind("\n")
		splitted.append(text[:index])
		for el in splitText(text[index + 1 :]):
			splitted.append(el)
		return splitted
	return [text]


# 	telegramSendMessage
# 	---------------------------------------------------------------------
# 	Sends the computed message to the user


def telegramSendMessage():
	global conn
	global finalMessage

	# If connection is correct and message is not empty, split text and send it
	if conn != None and finalMessage != "":
		for part in splitText(finalMessage):
			conn.send_message(chatId, f"`{part}`", parse_mode="MarkdownV2")

	# Reset the message
	finalMessage = ""
