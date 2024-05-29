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
from tkintermapview import TkinterMapView

from PlayerInformation import *
from SubWindow import *
from PCroom import PCInfo

#던전앤파이터용 데이터
api_server_d = "api.neople.co.kr"
api_image_server_d = "img-api.neople.co.kr"
service_key_d = "XseeTsrayJvhvwg8IATRWhpPXb2nZ2DP"

#경기도 pc방
api_server_pc = "openapi.gg.go.kr"
service_key_pc = "6a89a2e6edcd400a9bc460e5db75df65"

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
    InfomationWindow = CharacterInformation()
    PCroomList = []
    def __init__(self):
        window = Tk()
        window.title("-던-")
        window.geometry("800x600")
        window.resizable(False, False)
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
        self.backgroundphoto = PhotoImage(file="resource/1page.gif")
        self.imageCanvas = Canvas(self.frame1, width=800, height=600)
        self.imageCanvas.place(x=0, y=0)
        self.imageCanvas.create_image(0, 0, anchor='nw', image=self.backgroundphoto, tags='back')

        Label(self.frame1, text="서버 선택").place(x=50, y=30)
        self.selected_server = StringVar()
        self.selected_server.set("전체")
        server_options = set([self.Game_servers['rows'][i]['serverName'] for i in range(len(self.Game_servers['rows']))])
        t_list = list(server_options)
        t_list.insert(0, "전체")
        tkinter.ttk.Combobox(self.frame1, textvariable=self.selected_server, values=t_list).place(x=50, y=50)

        self.searchName = StringVar()
        self.searchEntry = Entry(self.frame1, textvariable=self.searchName, width= 25)
        Label(self.frame1, text="이름 입력").place(x=260, y=29)
        self.searchEntry.place(x=260, y = 50)
        self.searchEntry.bind("<Return>", self.searchCharEvent)
        Button(self.frame1, text="검색", command=self.searchChar).place(x=450, y=45)

        tframe = Frame(self.frame1, width=40, height=20)
        tframe.place(x=50, y=150)

        self.player_list = Listbox(tframe,width=35,height=20)
        self.player_list.pack(side=LEFT)
        self.Scrollbar = Scrollbar(tframe)
        self.Scrollbar.pack(side=RIGHT, fill=Y)
        self.player_list.config(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.config(command=self.player_list.yview)
        self.player_list.bind("<<ListboxSelect>>", self.selectListBoxEvent)
        #self.charImage = Label(self.frame1)


        self.searchButton = Button(self.frame1, text="정보 보기",width=10,height=2, command=self.searchAdvanced)
        self.searchButton['state'] = 'disabled'
        self.searchButton['bg'] = 'light gray'
        self.searchButton.place(x=130, y=500)
        
        
        # 2번 노트패드
        self.page2 = PhotoImage(file="resource/2page.png")
        Label(self.frame2, image=self.page2).place(x=0,y=0)
        Label(self.frame2,text='서버 선택').place(x=180, y=60)
        Label(self.frame2, text='명성 입력').place(x=350, y=60)
        Label(self.frame2, text='집계 범위는 입력 명성-2000까지며 미입력시 게임 내 가장 높은\n명성으로 입력명성이 결정됩니다(최고명성 초과입력 시 동일).').place(x=450, y=10)
        Label(self.frame2, text='(최대 200명의 플레이어 집계, 최소 55000이상 검색)').place(x=450, y=42)
        tkinter.ttk.Combobox(self.frame2, textvariable=self.selected_server, values=t_list).place(x=180, y=80)
        self.fameEntry = Entry(self.frame2, width=25,)
        self.fameEntry.place(x = 350, y=80)
        self.fameEntry.bind('<Return>', self.printGraphEvent)
        Button(self.frame2, text='검색', command=self.printGraph).place(x=535, y=75)
        self.graphCanvas = Canvas(self.frame2, width= 700, height=400, bg='gray79')
        self.graphCanvas.place(x=50, y=110)

        # 3번 노트패드
        conn = http.client.HTTPSConnection(api_server_pc)
        conn.request("GET", "/GameSoftwaresFacilityProvis?KEY=" + service_key_pc+"&Type=json&pIndex=&pSize")
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)['GameSoftwaresFacilityProvis'][1]['row']
        t_list.clear()
        for data in jsonData:
            if not data["SIGUN_NM"] in t_list:
                t_list.append(data["SIGUN_NM"])
        self.selected_SIGUN = StringVar()
        self.selected_SIGUN.set('파주시')
        SIGUN_NM = urllib.parse.quote('파주시')
        conn.request("GET", "/GameSoftwaresFacilityProvis?KEY=" + service_key_pc + "&Type=json&pIndex=&pSize&SIGUN_NM="+SIGUN_NM)
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)['GameSoftwaresFacilityProvis'][1]['row']
        self.PCCombo = tkinter.ttk.Combobox(self.frame3, textvariable=self.selected_SIGUN, values=t_list)
        self.PCCombo.place(x=140, y=80)
        self.PCCombo.bind("<<ComboboxSelected>>", self.loadPC)
        lframe = Frame(self.frame3, width=40, height=10)
        lframe.place(x=450,y=10)
        self.PCListbox = Listbox(lframe, width=35, height=10)
        self.PCListbox.pack(side=LEFT)
        self.PCScroll = Scrollbar(lframe)
        self.PCScroll.pack(side=RIGHT, fill=Y)
        self.PCListbox.config(yscrollcommand=self.PCScroll.set)
        self.PCScroll.config(command=self.PCListbox.yview)
        self.PCListbox.bind("<<ListboxSelect>>", self.selectPCList)

        self.map_widget = TkinterMapView(self.frame3, width=500, height=380, corner_radius=0)
        self.map_widget.pack(side=BOTTOM, anchor='se')
        self.search_marker = self.map_widget.set_position(37.7700000687, 126.7024211956, marker=True)
        self.search_marker.set_text("케이탑PC방")
        self.PCinfoFrame = Frame(self.frame3, width=300, height=500)
        self.PCinfoFrame.place(x=0, y=190)
        self.PCname = Label(self.PCinfoFrame, text='')
        self.PCname.pack()
        self.PCopenDate = Label(self.PCinfoFrame, text='')
        self.PCopenDate.pack()
        self.PCLOTNO = Label(self.PCinfoFrame, text='')
        self.PCLOTNO.pack()
        self.PCROADNM = Label(self.PCinfoFrame, text='')
        self.PCROADNM.pack()
        self.PCZIP = Label(self.PCinfoFrame, text='')
        self.PCZIP.pack()
        self.PCWGSX = Label(self.PCinfoFrame, text='')
        self.PCWGSX.pack()
        self.PCWGSY = Label(self.PCinfoFrame, text='')
        self.PCWGSY.pack()

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
        tt = self.player_list.curselection()
        if len(tt) == 0:
            return
        self.User.initBasicInfo(self.searchList['rows'][self.player_list.curselection()[0]])
        self.imageCanvas.delete('charIm')
        self.imageCanvas.create_image(550, 300, image=self.User.characterImage, tags='charIm')
        self.searchButton['state'] = 'active'
        self.searchButton['bg'] = 'white'

    def searchAdvanced(self):
        self.User.initAdvancedInfo()
        if self.InfomationWindow.isCreated:
            self.InfomationWindow.destroyWindow()
        self.InfomationWindow.initUserInfo(self.User)
        self.InfomationWindow.createWindow()
    def printGraphEvent(self, event):
        self.printGraph()
    def printGraph(self):
        if self.fameEntry.get() != '' and not self.fameEntry.get().isdigit():
            tkinter.messagebox.showerror('오류', '명성(숫자)를 입력해주세요!')
            return
        elif self.fameEntry.get() != '' and eval(self.fameEntry.get()) < 55000:
            tkinter.messagebox.showerror('오류', '최소 55000 이상을 입력하세요!')
            return
        if self.selected_server.get() == "전체":
            serverId = 'all'
        else:
            for i in range(len(self.Game_servers['rows'])):
                if self.selected_server.get() == self.Game_servers['rows'][i]['serverName']:
                    serverId = self.Game_servers['rows'][i]['serverId']
                    break
        maxFame = self.fameEntry.get()
        conn = http.client.HTTPSConnection(api_server_d)
        conn.request("GET", "/df/servers/"+serverId+"/characters-fame?minFame=&maxFame="+maxFame+"&jobId=&jobGrowId=&isAllJobGrow=&isBuff=&limit=200&apikey="+service_key_d)
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)
        fameDict = {"귀검사(남)":0, "귀검사(여)":0, "격투가(남)":0, "격투가(여)":0, "거너(남)":0,"거너(여)":0,
                    "마법사(남)":0,"마법사(여)":0,"프리스트(남)":0,"프리스트(여)":0,"도적":0,"나이트":0,"마창사":0,
                    "총검사":0,"아처":0,"다크나이트":0,"크리에이터":0}
        for data in jsonData['rows']:
            fameDict[data['jobName']] += 1
        self.graphCanvas.delete('graph')
        all_values = fameDict.values()
        max_job_cnt = max(all_values)
        bar_width = 20
        x_gap = 20
        x0 = 20
        y0 = 250
        icnt = 0
        for key, value in fameDict.items():
            x1 = x0 + icnt*(bar_width + x_gap)
            y1 = y0 - 200 * value / max_job_cnt
            self.graphCanvas.create_rectangle(x1, y1, x1+bar_width, y0, fill="red", tags='graph')
            self.graphCanvas.create_text(x1 + bar_width / 2, y0 + 100, text=key, anchor='n', angle=90, tags='graph')
            self.graphCanvas.create_text(x1 + bar_width / 2, y1 - 10, text=str(value), anchor='s', tags='graph')
            icnt += 1
    def loadPC(self, event):
        self.PCroomList.clear()
        SIGUN_NM = urllib.parse.quote(self.selected_SIGUN.get())
        conn = http.client.HTTPSConnection(api_server_pc)
        conn.request("GET", "/GameSoftwaresFacilityProvis?KEY=" + service_key_pc + "&Type=json&pIndex=&pSize&SIGUN_NM="+SIGUN_NM)
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)['GameSoftwaresFacilityProvis'][1]['row']
        for data in jsonData:
            if data["BSN_STATE_NM"] == '운영중':
                newPC = PCInfo(data['SIGUN_CD'], data['SIGUN_NM'], data['BIZPLC_NM'], data['LICENSG_DE'], data['REFINE_LOTNO_ADDR'], data['REFINE_ROADNM_ADDR'], data['REFINE_ZIP_CD'], data['REFINE_WGS84_LAT'], data['REFINE_WGS84_LOGT'])
                self.PCroomList.append(newPC)
        self.PCListbox.delete(0, END)
        for i in range(len(self.PCroomList)):
            self.PCListbox.insert(i+1, self.PCroomList[i].BIZPLC_NM)
    def selectPCList(self,event):
        tt = self.PCListbox.curselection()
        if len(tt) == 0:
            return
        tt = self.PCListbox.curselection()[0]
        self.map_widget.delete(self.search_marker)
        self.search_marker = self.map_widget.set_position(eval(self.PCroomList[tt].WGS_LAT), eval(self.PCroomList[tt].WGS_LOGT), marker=True)
        self.search_marker.set_text(self.PCroomList[tt].BIZPLC_NM)

        self.PCname.configure(text="시설 이름: "+self.PCroomList[tt].BIZPLC_NM)
        self.PCopenDate.configure(text='오픈날: ' + self.PCroomList[tt].LICENSG_DE)
        self.PCLOTNO.config(wraplength=300)
        self.PCLOTNO.configure(text='지번주소: ' + self.PCroomList[tt].LONTO_ADDR)
        self.PCROADNM.config(wraplength=300)
        self.PCROADNM.configure(text="도로명주소: "+self.PCroomList[tt].ROADNM_ADDR)
DUN()