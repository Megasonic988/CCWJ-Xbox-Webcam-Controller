import subprocess
import pygame

def runCommand(command):
    commandArray = command.split()
    return subprocess.Popen(commandArray)

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

BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

pygame.init()
size = [500, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('CCWJ Camera Controller')
done = False
clock = pygame.time.Clock()
pygame.joystick.init()
textPrint = TextPrint()
joystick_index = 0

# control = brightness
# control.changeValue(value*0.5)
# control = saturation
# control.changeValue(hatValue[0]*5)
# control = white_balance
# runCommand('v4l2-ctl --set-ctrl white_balance_temperature_auto=0')
# control.changeValue(hatValue[1]*200)
# control = sharpness
# control.changeValue(5)
# control = gain
# control.changeValue(5)

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

def startRecording(video, audio, welder, operator, process):
    return runCommand('ffmpeg -f video4linux2 -r 25 -i ' + video + ' -f alsa -i ' + audio + ' -acodec aac -vcodec mpeg4 -y ' + welder + operator + process + '.mp4')

# main joystick input loop
def controllerLoop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.fill(WHITE)
    textPrint.reset()

    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print('No joysticks found!')
        return

    joystick = pygame.joystick.Joystick(joystick_index)
    joystick.init()

    name = joystick.get_name()
    textPrint.print(screen, "Joystick name: {}".format(name))

    axes = joystick.get_numaxes()
    textPrint.print(screen, "Number of axes: {}".format(axes))

    textPrint.indent()
    for i in range(axes):
        axisValue = joystick.get_axis(i)
        axisName = axisNameForIndex(i)
        textPrint.print(screen, "{} Axis value: {:>6.3f}".format(axisName, axisValue))
        handleAxisInput(axisName, axisValue)
    textPrint.unindent()

    buttons = joystick.get_numbuttons()
    textPrint.print(screen, "Number of buttons: {}".format(buttons))

    textPrint.indent()
    for i in range(buttons):
        button = joystick.get_button(i)
        buttonName = buttonNameForIndex(i)
        textPrint.print(screen, "{} Button: {}".format(buttonName, button))
        handleButtonInput(buttonName, button)
        if (buttonName == 'Guide' and button == 1):
            done = True
    textPrint.unindent()

    # Value comes back in an array.
    hats = joystick.get_numhats()
    textPrint.print(screen, "Number of hats: {}".format(hats))

    textPrint.indent()
    hat = joystick.get_hat(0)
    textPrint.print(screen, "Hat {} value: {}".format(0, str(hat)))
    handleHatInput(hat)
    textPrint.unindent()

    pygame.display.flip()
    clock.tick(100)

# pygame.quit()
