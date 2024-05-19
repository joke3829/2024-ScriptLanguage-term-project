import http.client
from PIL import Image, ImageTk
from io import  BytesIO
import urllib
import urllib.request
import urllib.parse
import json

api_server_d = "api.neople.co.kr"
api_image_server_d = "img-api.neople.co.kr"
service_key_d = "XseeTsrayJvhvwg8IATRWhpPXb2nZ2DP"

class PlayerInformation:
    def initBasicInfo(self, jsonData): # 기본 정보들
        self.playerjson = jsonData
        self.serverId = jsonData['serverId']
        self.characterId = jsonData['characterId']
        self.characterName = jsonData['characterName']
        self.level = jsonData['level']
        self.jobId = jsonData['jobId']
        self.jobGrowId = jsonData['jobGrowId']
        self.jobName =jsonData['jobName']
        self.jobGrowName = jsonData['jobGrowName']
        self.fame = jsonData['fame']
        # 캐릭터 이미지 읽기 및 저장
        url = "https://"+api_image_server_d+"/df/servers/"+self.serverId+"/characters/"+self.characterId+"?zoom=2"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.characterImage = ImageTk.PhotoImage(im)

    def initAdvancedInfo(self):
        #장비 정보 받기
        conn = http.client.HTTPSConnection(api_server_d)
        conn.request("GET", "/df/servers/"+self.serverId+"/characters/"+self.characterId+"/equip/equipment?apikey="+service_key_d)
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)
        equimentjson = jsonData['equipment']
        print(equimentjson)

class equipment:
    def initEqInfo(self):
        pass

class WEAPON:       # 무기
    def initWeaponInfo(self):
        pass

class DEFENSEGEAR:
    def initDEFInfo(self):
        pass