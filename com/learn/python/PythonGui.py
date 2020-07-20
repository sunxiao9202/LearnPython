from tkinter import *
from tkinter import messagebox


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.nameInput = Entry(self)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput.pack()
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)


app = Application()

app.master.title('Hello World')
app.mainloop()
