from tkinter import *
from tkinter.ttk import *
import controller

video = ''
audio = ''

class WebcamControllerApp(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.welder = StringVar()
        self.operator = StringVar()
        self.process = StringVar()

        self.initUI()

    def initUI(self):

        self.parent.title("CCWJ Welding Helmet Controller")
        self.style = Style()
        self.style.theme_use("clam")

        self.pack(fill=BOTH, expand=True)

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        frame1 = Frame(frame)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Welder Name", width=15)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        entry1 = Entry(frame1, textvariable=self.welder)
        entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(frame)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Operator Name", width=15)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = Entry(frame2, textvariable=self.operator)
        entry2.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(frame)
        frame3.pack(fill=X)

        lbl3 = Label(frame3, text="Process", width=15)
        lbl3.pack(side=LEFT, padx=5, pady=5)

        entry3 = Entry(frame3, textvariable=self.process)
        entry3.pack(fill=X, padx=5, expand=True)

        self.recordButton = Button(self, text="Start Record", command=self.startRecording)
        self.recordButton.pack(side=RIGHT, padx=5, pady=5)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.pack(side=RIGHT)

    def startRecording(self):
        print('recording')
        self.recordButton.config(text='Stop Record', command=self.stopRecording)
        self.recordingProcess = controller.startRecording(video, audio, self.welder, self.operator, self.process)

    def stopRecording(self):
        print('stopped recording')
        self.recordingProcess.kill()
        self.recordButton.config(text='Start Record', command=self.startRecording)


def main():

    root = Tk()
    root.geometry("400x200+300+300")
    app = WebcamControllerApp(root)

    def controllerLoop():
        controller.controllerLoop()
        root.after(10, controllerLoop)

    root.after(0, controllerLoop)
    root.mainloop()



if __name__ == '__main__':
    main()
