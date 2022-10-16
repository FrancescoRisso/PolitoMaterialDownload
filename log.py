from telegram import telegramLog
import time

telegramConnected = False
tmpLog = []

# 	log
# 	---------------------------------------------------------------------
# 	Prints a log to console
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- type: the type of message (INFO | ERR | SAVE)
# 		- message: the text to be printed


def log(type, message):
	global tmpLog

	# Compute the message text in the format "[type] message"
	mess = f"[{type:4}] {message}"

	# Append message to the telegram message, if it is connected, else append
	# the message to the temporary string
	if telegramConnected:
		try:
			telegramLog(mess, type)
		except Exception:
			log("ERR", "Bot is not connected")
	else:
		tmpLog.append((mess, type))

	# Log the message with its time to console
	print(f"{time.strftime('%Y-%m-%d %H:%M:%S').format()} {mess}", flush=True)


# 	changeTelegramConn
# 	---------------------------------------------------------------------
# 	Changes the current information about the telegram connection to the
# 	bot
# 	---------------------------------------------------------------------
# 	PARAMETERS:
# 		- nowIsConnected: whether at time of function call the bot is
# 			correctly connected


def LOGchangeTelegramConn(nowIsConnected):
	global telegramConnected
	global tmpLog

	# If telegram was not connected, and now is, send the old log
	if nowIsConnected and not telegramConnected:
		for l in tmpLog:
			telegramLog(l[0], l[1])
		telegramConnected = True

	# If telegram disconnected, reset the temporary log
	if not nowIsConnected:
		tmpLog = []
