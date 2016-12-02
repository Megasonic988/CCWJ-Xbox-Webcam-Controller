import subprocess
import pygame
import time

def runCommand(command):
    subprocess.Popen(command, shell=True)

class CameraControl:
    def __init__(self, name, default, min, max):
        self.name = name
        self.value = default
        self.min = min
        self.max = max

    def increaseBy(self, value):
        self.value += value
        if self.value > self.max:
            self.value = self.max

    def decreaseBy(self, value):
        self.value -= value
        if self.value < self.min:
            self.value = self.min

    def changeValue(self, value):
        if value > 0:
            self.increaseBy(value)
        if value < 0:
            self.decreaseBy(abs(value))

    def getValue(self):
        return str(round(self.value))

    def getName(self):
        return self.name

'''Controls: CameraControl(name, default, min, max)'''
brightness = CameraControl('brightness', 128, 0, 255)
contrast = CameraControl('contrast', 32, 0, 255)
saturation = CameraControl('saturation', 34, 0, 255)
gain = CameraControl('gain', 64, 0, 255)
white_balance = CameraControl('white_balance_temperature', 4000, 2800, 6500)
sharpness = CameraControl('sharpness', 22, 0, 255)
exposure = CameraControl('exposure_absolute', 166, 3, 2047)
pan = CameraControl('pan_absolute', 0, -36000, 36000) # pan is X axis, step 3600
tilt = CameraControl('tilt_absolute', 0, -36000, 36000) # tilt is Y axis, step 3600
zoom = CameraControl('zoom_absolute', 1, 1, 5)

pygame.init()
pygame.joystick.init()
joystick_index = 0
runCommand('killall guvcview')
time.sleep(0.5) # must sleep to give killall some time
runCommand('guvcview --gui=none --audio=pulse --audio_device=0')
time.sleep(1.2)
runCommand('wmctrl -r "Guvcview" -b add,maximized_vert,maximized_horz')
runCommand('wmctrl -a "CCWJ Welding Helmet Controller"')

def buttonNameForIndex(i):
    if i == 0: return 'A'
    elif i == 1: return 'B'
    elif i == 2: return 'X'
    elif i == 3: return 'Y'
    elif i == 4: return 'Right Bumper'
    elif i == 5: return 'Left Bumper'
    elif i == 6: return 'Back'
    elif i == 7: return 'Start'
    elif i == 8: return 'Guide'
    elif i == 9: return 'Left Stick'
    elif i == 10: return 'Right Stick'
    else: raise ValueError("Error: invalid button configuration")

def axisNameForIndex(i):
    if i == 0: return 'Left Stick X'
    elif i == 1: return 'Left Stick Y'
    elif i == 2: return 'Right Stick X'
    elif i == 3: return 'Right Stick Y'
    elif i == 4: return 'Right Trigger'
    elif i == 5: return 'Left Trigger'
    else: raise ValueError("Error: invalid stick configuration")

def activatePreset(preset):
    if preset == 'MIG':
	    pass
    if preset == 'TIG':
	    pass
    if preset == 'Stick':
	    pass
    if preset == 'Flux Cored Wire':
        pass

def handleAxisInput(axisName, value):
    control = None
    if axisName == 'Left Stick X' and abs(value) > 0.2:
        pass
    if axisName == 'Left Stick Y' and abs(value) > 0.2:
        control = zoom
        control.changeValue(-0.1)
    if axisName == 'Left Trigger' and value > 0.7:
        pass
    if axisName == 'Right Trigger' and value > 0.7:
        pass
    if axisName == 'Right Stick X' and abs(value) > 0.5:
        control = pan
        control.changeValue(value*10000)
    if axisName == 'Right Stick Y' and abs(value) > 0.5:
        control = tilt
        control.changeValue(value*10000)
    if control != None:
        runCommand('v4l2-ctl --set-ctrl ' + control.getName() + '=' + control.getValue())

def handleHatInput(hatValue):
    control = None
    if hatValue[0] == -1 or hatValue[0] == 1: #X axis
        control = contrast
        control.changeValue(hatValue[0]*0.5)
    if hatValue[1] == -1 or hatValue[1] == 1: #Y axis
        control = brightness
        control.changeValue(hatValue[1]*0.5)
    if control != None:
        runCommand('v4l2-ctl --set-ctrl ' + control.getName() + '=' + control.getValue())

def handleButtonInput(buttonName, value):
    control = None
    if value == 0:
        return
    if buttonName == 'Left Bumper':
        control = exposure
        runCommand('v4l2-ctl --set-ctrl exposure_auto=1')
        control.changeValue(50)
    if buttonName == 'Right Bumper':
        control = exposure
        runCommand('v4l2-ctl --set-ctrl exposure_auto=1')
        control.changeValue(-50)
    if buttonName == 'A':
        activatePreset('MIG')
    if buttonName == 'B':
        activatePreset('TIG')
    if buttonName == 'X':
        activatePreset('Stick')
    if buttonName == 'Y':
        activatePreset('Flux Cored Wire')
    if control != None:
        runCommand('v4l2-ctl --set-ctrl ' + control.getName() + '=' + control.getValue())

def startRecording():
    runCommand('killall -SIGUSR1 guvcview')

def stopRecording(welder, operator, process):
    runCommand('killall -SIGUSR1 guvcview')
    time.sleep(0.5)
    filename_items = ['CCWJ']
    if welder:
        filename_items.append(welder.replace(' ', ''))
    if operator:
        filename_items.append(operator.replace(' ', ''))
    if process:
        filename_items.append(process.replace(' ', ''))
    filename_items.append(time.strftime("%b-%d-%Y_%H-%M-%S"))
    filename = '_'.join(filename_items)
    runCommand('mv /home/clac/my_video-1.mkv ' + 'Output/' + filename + '.mkv')

def quit():
    runCommand('killall guvcview')

# main joystick input loop
def controllerLoop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print('No joysticks found!')
        exit()

    joystick = pygame.joystick.Joystick(joystick_index)
    joystick.init()

    axes = joystick.get_numaxes()
    for i in range(axes):
        axisValue = joystick.get_axis(i)
        axisName = axisNameForIndex(i)
        handleAxisInput(axisName, axisValue)

    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        button = joystick.get_button(i)
        buttonName = buttonNameForIndex(i)
        handleButtonInput(buttonName, button)

    # Value comes back in an array.
    hats = joystick.get_numhats()
    hat = joystick.get_hat(0)
    handleHatInput(hat)
