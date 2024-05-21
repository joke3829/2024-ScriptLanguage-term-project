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
        self.window.resizable(False, False)
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
        #배경 이미지 및 배치
        image = Image.open("resource/World_of_Rumination.png")
        iimage = image.resize((1742, 800))
        self.page1_back = ImageTk.PhotoImage(iimage, master=self.window)
        self.CharCanvas = Canvas(self.frame1, width=600, height=800, bg='white')
        self.CharCanvas.pack()
        self.CharCanvas.create_image(-556, 0, anchor='nw', image=self.page1_back, tags='back')
        #캐릭터 이미지 및 배치
        with urllib.request.urlopen(self.User.smallurl) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((300, 345))
        self.smallChar = ImageTk.PhotoImage(im, master=self.window)
        self.CharCanvas.create_image(150, -50, anchor='nw', image=self.smallChar, tags='char')

        #무기 라벨
        if self.User.m_equipment[0].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[0].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.WeaponImage = ImageTk.PhotoImage(im, master=self.window)
            self.WeaponLabel = Label(self.frame1, image=self.WeaponImage)
            self.WeaponLabel.bind("<Button-1>", self.showWeaponInfo)
            self.WeaponLabel.place(x= 420, y=42)
        # 칭호 라벨
        if self.User.m_equipment[1].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[1].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.TitleImage = ImageTk.PhotoImage(im, master=self.window)
            self.TitleLabel = Label(self.frame1, image=self.TitleImage)
            self.TitleLabel.bind("<Button-1>", self.showTitleInfo)
            self.TitleLabel.place(x= 475, y=42)
        # 상의 라벨
        if self.User.m_equipment[2].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[2].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.JacketImage = ImageTk.PhotoImage(im, master=self.window)
            self.JacketLabel = Label(self.frame1, image=self.JacketImage)
            self.JacketLabel.bind("<Button-1>", self.showJacketInfo)
            self.JacketLabel.place(x= 130, y=42)
        # 어깨 라벨
        if self.User.m_equipment[3].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[3].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.ShoulderImage = ImageTk.PhotoImage(im, master=self.window)
            self.ShoulderLabel = Label(self.frame1, image=self.ShoulderImage)
            self.ShoulderLabel.bind("<Button-1>", self.showShoulderInfo)
            self.ShoulderLabel.place(x= 75, y=42)
        # 하의
        if self.User.m_equipment[4].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[4].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.PantsImage = ImageTk.PhotoImage(im, master=self.window)
            self.PantsLabel = Label(self.frame1, image=self.PantsImage)
            self.PantsLabel.bind("<Button-1>", self.showPantsInfo)
            self.PantsLabel.place(x= 75, y=97)
        # 신발
        if self.User.m_equipment[5].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[5].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.ShoesImage = ImageTk.PhotoImage(im, master=self.window)
            self.ShoesLabel = Label(self.frame1, image=self.ShoesImage)
            self.ShoesLabel.bind("<Button-1>", self.showShoesInfo)
            self.ShoesLabel.place(x= 75, y=152)
        # 벨트
        if self.User.m_equipment[6].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[6].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.WaistImage = ImageTk.PhotoImage(im, master=self.window)
            self.WaistLabel = Label(self.frame1, image=self.WaistImage)
            self.WaistLabel.bind("<Button-1>", self.showWaistInfo)
            self.WaistLabel.place(x= 130, y=97)
        # 목걸이
        if self.User.m_equipment[7].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[7].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.AmuletImage = ImageTk.PhotoImage(im, master=self.window)
            self.AmuletLabel = Label(self.frame1, image=self.AmuletImage)
            self.AmuletLabel.bind("<Button-1>", self.showAmuletInfo)
            self.AmuletLabel.place(x= 475, y=97)
        # 팔찌
        if self.User.m_equipment[8].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[8].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.WristImage = ImageTk.PhotoImage(im, master=self.window)
            self.WristLabel = Label(self.frame1, image=self.WristImage)
            self.WristLabel.bind("<Button-1>", self.showWristInfo)
            self.WristLabel.place(x= 420, y=97)
        # 반지
        if self.User.m_equipment[9].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[9].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.RingImage = ImageTk.PhotoImage(im, master=self.window)
            self.RingLabel = Label(self.frame1, image=self.RingImage)
            self.RingLabel.bind("<Button-1>", self.showRingInfo)
            self.RingLabel.place(x= 475, y=152)
        # 보조장비
        if self.User.m_equipment[10].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[10].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.SupportImage = ImageTk.PhotoImage(im, master=self.window)
            self.SupportLabel = Label(self.frame1, image=self.SupportImage)
            self.SupportLabel.bind("<Button-1>", self.showSupportInfo)
            self.SupportLabel.place(x= 420, y=152)
        # 마법석
        if self.User.m_equipment[11].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[11].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.MagicSImage = ImageTk.PhotoImage(im, master=self.window)
            self.MagicSLabel = Label(self.frame1, image=self.MagicSImage)
            self.MagicSLabel.bind("<Button-1>", self.showMagicSInfo)
            self.MagicSLabel.place(x= 475, y=207)
        # 귀걸이
        if self.User.m_equipment[12].isequip:
            url = "https://img-api.neople.co.kr/df/items/" + self.User.m_equipment[12].itemId
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((50, 50))
            self.EarringImage = ImageTk.PhotoImage(im, master=self.window)
            self.EarringLabel = Label(self.frame1, image=self.EarringImage)
            self.EarringLabel.bind("<Button-1>", self.showEarringInfo)
            self.EarringLabel.place(x= 420, y=207)
        # 보조 무기(시간 남으면)

    def ReadyStatPage(self):
        pass
    def ReadyTimelinePage(self):
        pass
    def showWeaponInfo(self, event):
        print("무기")
    def showTitleInfo(self, event):
        print("칭호")
    def showJacketInfo(self, event):
        print("상의")
    def showShoulderInfo(self, event):
        print("어깨")
    def showPantsInfo(self, event):
        print("하의")
    def showShoesInfo(self, event):
        print("신발")
    def showWaistInfo(self, event):
        print("벨트")
    def showAmuletInfo(self, event):
        print("목걸이")
    def showWristInfo(self, event):
        print("팔찌")

    def showRingInfo(self, event):
        print("반지")
    def showSupportInfo(self, event):
        print("보조장비")
    def showMagicSInfo(self, event):
        print("마법석")
    def showEarringInfo(self, event):
        print("귀걸이")
    def destroyWindow(self):
        self.CharCanvas.delete('back')
        self.CharCanvas.destroy()

        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()

        self.window.destroy()
        self.isCreated = False