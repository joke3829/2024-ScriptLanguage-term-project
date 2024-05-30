from tkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PlayerInformation import *

class mailBox:
    User = None
    isCreate = False
    def initUser(self, u):
        self.User = u
    def createWindow(self):
        self.isCreate = True
        self.window = Tk()
        self.window.title("메일 박스")
        self.window.geometry("350x200")
        self.window.protocol("WM_DELETE_WINDOW", self.destroyWindow)

        Label(self.window, text="보내는 사람 gmail 주소 입력").place(x=20, y=20)
        self.senderEntry = Entry(self.window, width=40)
        self.senderEntry.place(x=20, y=40)
        Label(self.window, text="받는 사람 메일 주소 입력").place(x=20, y=60)
        self.reEntry = Entry(self.window, width=40)
        self.reEntry.place(x=20, y=80)
        Label(self.window, text="앱 비밀번호 입력").place(x=20, y=100)
        self.PassEntry = Entry(self.window, width=30, show="*")
        self.PassEntry.place(x=20,y=120)

        Button(self.window, text="메일 발송", command=self.sendmail).place(x= 280, y=150)
        self.bottomlabel = Label(self.window, text="")
        self.bottomlabel.place(x=20, y=150)

        self.window.mainloop()
    def sendmail(self):
        if self.senderEntry.get() == "" or self.reEntry.get() == "" or self.PassEntry.get() == "":
            self.bottomlabel.configure(text="모든 칸을 채워주세요")
            return
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(self.senderEntry.get(), self.PassEntry.get())

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.User.characterName +"의 정보"
        msg["From"] = self.senderEntry.get()
        msg["To"] = self.reEntry.get()
        html = self.MakeHtmlDoc()

        msgtext= MIMEText(html, 'html', _charset='UTF-8')
        msg.attach(msgtext)

        s.sendmail(self.senderEntry.get(), [self.reEntry.get()], msg.as_string())
        s.close()
        self.destroyWindow()


    def MakeHtmlDoc(self):
        from xml.dom.minidom import getDOMImplementation
        # get Dom Implementation
        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
        top_element = newdoc.documentElement
        header = newdoc.createElement('header')
        top_element.appendChild(header)

        # Body 엘리먼트 생성.
        body = newdoc.createElement('body')

        p = newdoc.createElement('p')
        serverAndName = newdoc.createTextNode("서버: "+ self.User.serverId+", 캐릭터 이름: "+self.User.characterName)
        p.appendChild(serverAndName)
        body.appendChild(p)
        br = newdoc.createElement('br')

        p = newdoc.createElement('p')
        LevelAndJob = newdoc.createTextNode("레벨: "+str(self.User.level) +", 직업: "+self.User.jobName+", 전직: "+self.User.jobGrowName)
        p.appendChild(LevelAndJob)
        body.appendChild(p)
        body.appendChild(br)

        for equip in self.User.m_equipment:
            if equip.isequip:
                p = newdoc.createElement('p')
                equipName = newdoc.createTextNode(equip.slotName+" - "+equip.itemName)
                p.appendChild(equipName)
                body.appendChild(p)
        # append Body
        top_element.appendChild(body)

        return newdoc.toxml()


    def destroyWindow(self):
        self.bottomlabel.destroy()
        self.window.destroy()
        self.isCreate = False