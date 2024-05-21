from tkinter import *
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
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
        self.window.protocol("WM_DELETE_WINDOW", self.destroyWindow)

        notebook = tkinter.ttk.Notebook(self.window, width=600, height=800)
        notebook.pack()
        self.frame1 = Frame(self.window)
        notebook.add(self.frame1, text='장비')

        self.frame2 = Frame(self.window)
        notebook.add(self.frame2, text='스텟')

        self.frame3 = Frame(self.window)
        notebook.add(self.frame3, text='타임라인')

        self.ReadyEquipmentPage()

        self.window.mainloop()
    def ReadyEquipmentPage(self):
        #self.page1_back = PhotoImage(file="resource/World_of_Rumination.png", master=self.window)
        image = Image.open("resource/World_of_Rumination.png")
        iimage = image.resize((1742, 800))
        self.page1_back = ImageTk.PhotoImage(iimage, master=self.window)
        self.CharCanvas = Canvas(self.frame1, width=600, height=800, bg='white')
        print(self.User.smallurl)
        self.CharCanvas.pack()
        self.CharCanvas.create_image(-556, 0, anchor='nw', image=self.page1_back, tags='back')

    def ReadyStatPage(self):
        pass
    def ReadyTimelinePage(self):
        pass
    def destroyWindow(self):
        self.CharCanvas.delete('back')
        self.CharCanvas.destroy()

        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()

        self.window.destroy()
        self.isCreated = False