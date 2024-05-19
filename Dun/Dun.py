import http.client
from tkinter import *
import tkinter.ttk
import tkinter.simpledialog
from io import  BytesIO
import urllib
import urllib.request
import urllib.parse
import json
from PIL import Image,ImageTk

from PlayerInformation import *
from SubWindow import *

#던전앤파이터용 데이터
api_server_d = "api.neople.co.kr"
api_image_server_d = "img-api.neople.co.kr"
service_key_d = "XseeTsrayJvhvwg8IATRWhpPXb2nZ2DP"

#던전앤파이터 검색용 요소들
serverId = ""
characterName = ""
jobId = ""
jobGrowld = ""
isAllJobGrow =""
wordType = ""
limit = ""

#PC방 정보용 데이터

class DUN:
    User = PlayerInformation()
    def __init__(self):
        window = Tk()
        window.title("-던-")
        notebook = tkinter.ttk.Notebook(window, width= 800, height=600)
        notebook.pack()
        self.frame1 = Frame(window)
        notebook.add(self.frame1, text="캐릭터 검색")


        self.frame2 = Frame(window)
        notebook.add(self.frame2, text="명성 직업 통계")

        self.frame3 = Frame(window)
        notebook.add(self.frame3, text="PC방 찾기")


        self.ReadyDNFServer()
        self.ReadyInterface()

        window.mainloop()
    def ReadyDNFServer(self):
        conn = http.client.HTTPSConnection(api_server_d)
        conn.request("GET", "/df/servers?apikey=" + service_key_d)
        result = conn.getresponse().read().decode("utf-8")
        self.Game_servers = json.loads(result)
        #Game_servers['rows'][0]['serverId'] = cain
    def ReadyInterface(self):
        # 1번 노트패드
        Label(self.frame1, text="서버 선택").place(x=50, y=30)
        self.selected_server = StringVar()
        self.selected_server.set("전체")
        server_options = set([self.Game_servers['rows'][i]['serverName'] for i in range(len(self.Game_servers['rows']))])
        t_list = list(server_options)
        t_list.insert(0, "전체")
        tkinter.ttk.Combobox(self.frame1, textvariable=self.selected_server, values=t_list).place(x=50, y=50)

        self.searchName = StringVar()
        self.searchEntry = Entry(self.frame1, textvariable=self.searchName, width= 40)
        self.searchEntry.place(x=260, y = 50)
        self.searchEntry.bind("<Return>", self.searchCharEvent)
        Button(self.frame1, text="검색", command=self.searchChar).place(x=550, y=45)

        tframe = Frame(self.frame1, width=40, height=20)
        tframe.place(x=50, y=150)

        self.player_list = Listbox(tframe,width=35,height=20)
        self.player_list.pack(side=LEFT)
        self.Scrollbar = Scrollbar(tframe)
        self.Scrollbar.pack(side=RIGHT, fill=Y)
        self.player_list.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.player_list.yview)
        self.player_list.bind("<<ListboxSelect>>", self.selectListBoxEvent)
        self.charImage = Label(self.frame1)

        self.searchButton = Button(self.frame1, text="정보 보기",width=10,height=2, command=self.searchAdvanced)
        self.searchButton['state'] = 'disabled'
        self.searchButton['bg'] = 'light gray'
        self.searchButton.place(x=130, y=500)

    def searchCharEvent(self, event):
        self.searchChar()
    def selectListBoxEvent(self, event):
        self.selectPlayer()
    def searchChar(self): #검색 버튼을 누르면 검색된 캐릭터들을 리스트 박스에 출력한다.
        if self.searchName.get() == "":
            tkinter.messagebox.showerror('오류', '이름을 입력하세요!')
            return
        elif len(self.searchName.get()) < 2:
            tkinter.messagebox.showerror('오류', '두글자 이상 입력하세요!')
            return
        if self.selected_server.get() == "전체":
            serverId = 'all'
        else:
            for i in range(len(self.Game_servers['rows'])):
                if self.selected_server.get() == self.Game_servers['rows'][i]['serverName']:
                    serverId = self.Game_servers['rows'][i]['serverId']
                    break
        characterName = urllib.parse.quote(self.searchName.get())
        jobId = ""
        jobGrowld = ""
        isAllJobGrow = ""
        wordType = "full"
        limit = "200"
        conn = http.client.HTTPSConnection(api_server_d)
        conn.request("GET", "/df/servers/"+serverId+"/characters?characterName="+characterName+"&jobId="+jobId+"&jobGrowId="+jobGrowld+"&isAllJobGrow="+isAllJobGrow+"&limit="+limit+"&wordType="+wordType+"&apikey="+service_key_d)
        result = conn.getresponse().read().decode("utf-8")
        self.searchList = json.loads(result)
        self.player_list.delete(0, END)
        for i in range(len(self.searchList['rows'])):
            for j in range(len(self.Game_servers['rows'])):
                if self.Game_servers['rows'][j]['serverId'] == self.searchList['rows'][i]['serverId']:
                    servername = self.Game_servers['rows'][j]['serverName']
                    break
            self.player_list.insert(i + 1, servername +", 명성:"+str(self.searchList['rows'][i]['fame'])+ ", 이름: "+
                                    self.searchList['rows'][i]['characterName'])
    def selectPlayer(self):
        self.User.initBasicInfo(self.searchList['rows'][self.player_list.curselection()[0]])
        self.charImage.destroy()
        self.charImage = Label(self.frame1, image=self.User.characterImage, bg="white")
        self.charImage.Image = self.User.characterImage
        self.charImage.place(x = 350, y = 100)
        self.searchButton['state'] = 'active'
        self.searchButton['bg'] = 'white'

    def searchAdvanced(self):
        self.User.initAdvancedInfo()






DUN()