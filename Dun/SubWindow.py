from tkinter import *
import tkinter.ttk
from PlayerInformation import *

class CharacterInformation: # 이 클래스는 검색한 캐리터의 정보를 가지는 PlayerInformation 클래스를 기지고 있다
    User = PlayerInformation()
    isCreated = False
    def initUserInfo(self, info):
        self.User = info
    def createWindow(self):
        self.isCreated = True
        self.window = Tk()
        self.window.title(self.User.characterName + "의 정보창")
        self.window.geometry("600x800")

        notebook = tkinter.ttk.Notebook(self.window, width=600, height=800)
        notebook.pack()
        self.frame1 = Frame(self.window)
        notebook.add(self.frame1, text='장비')

        self.frame2 = Frame(self.window)
        notebook.add(self.frame2, text='스텟')

        self.frame3 = Frame(self.window)
        notebook.add(self.frame3, text='타임라인')



        self.window.mainloop()

    def destroyWindow(self):
        self.window.destroy()
        self.isCreated = False

