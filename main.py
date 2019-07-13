import pyautogui, ctypes, sys
from pynput import keyboard

# Globals
winUser = ctypes.windll.user32
primaryWidth = winUser.GetSystemMetrics(0)
primaryHeight = winUser.GetSystemMetrics(1)
currentScreen = None
currentLastPos = None
prevLastPos = None


def listenForKeyPress():
	monitorCount = ctypes.windll.user32.GetSystemMetrics(80)
	if monitorCount < 2:
		print('Not enough monitors detected')
		sys.exit()

	# Collect events until released
	with keyboard.Listener(
		on_press=on_press) as listener:
		listener.join()


def on_press(key):
	try: 
		if key.name == 'caps_lock':
			global currentScreen
			currentMouseX, currentMouseY = pyautogui.position()

			if currentMouseX > primaryWidth:
				# Cursor is on secondary screen
				if currentScreen != 'secondary':
					currentScreen = 'secondary'
					updateLastPosAndSwitch(currentMouseX, currentMouseY)
			else:
				# Cursor is on primary screen
				if currentScreen != 'primary':
					currentScreen = 'primary'
					updateLastPosAndSwitch(currentMouseX, currentMouseY)
	except:
		# Key has no attribute "name"
		pass


def updateLastPosAndSwitch(currentMouseX, currentMouseY):
	global currentLastPos, prevLastPos

	# update lastPos for current screen
	currentLastPos = {
		'x': currentMouseX,
		'y': currentMouseY
	}

	# Try to switch to lastPos
	if prevLastPos:
		pyautogui.moveTo(prevLastPos['x'], prevLastPos['y'])

	prevLastPos = currentLastPos


if __name__ == '__main__':
	listenForKeyPress()