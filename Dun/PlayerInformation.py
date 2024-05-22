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


equipmentEnum = {"WEAPON": 0, "TITLE": 1, "JACKET" : 2, "SHOULDER": 3, "PANTS": 4
                 , "SHOES": 5, "WAIST": 6, "AMULET": 7, "WRIST": 8, "RING": 9
                 , "SUPPORT": 10, "MAGIC_STON": 11, "EARRING": 12, "SUPPORT_WEAPON": 13}


class equipment:        # 장비가 공통적으로 가지는 요소
    isequip = False     # 이 장비를 장착 했나?
    isenchant = False   # 마법 부여 여부
    slotId = ""
    slotName = ""
    itemId = ""
    itemName = ""
    itemTypeId = ""
    itemType = ""
    itemTypeDetailId = ""
    itemTypeDetail = ""
    itemAvailableLevel = 0  # 징칙 레벨
    itemRarity = ""         # 레어도(에픽)
    setItemId = ""
    setItemName = ""        # 세트 이름
    reinforce = 0           # 강화 수치
    amplificationName = ""  # 증폭 여부
    refine = ""             # 재련 수치

    equipmentImageUrl = ""  # 장비 이미지 url

    def initEqInfo(self, jsonData):
        self.isequip = True
        self.slotId = jsonData['slotId']
        self.slotName = jsonData['slotName']
        self.itemId = jsonData['itemId']
        self.itemName = jsonData['itemName']
        self.itemTypeId = jsonData['itemTypeId']
        self.itemType = jsonData['itemType']
        self.itemTypeDetailId = jsonData['itemTypeDetailId']
        self.itemTypeDetail = jsonData['itemTypeDetail']
        self.itemAvailableLevel = jsonData['itemAvailableLevel']
        self.itemRarity = jsonData['itemRarity']
        self.setItemId = jsonData['setItemId']
        self.setItemName = jsonData['setItemName']
        self.reinforce = jsonData['reinforce']
        self.amplificationName = jsonData['amplificationName']
        self.refine = jsonData['refine']

        self.equipmentImageUrl = "https://"+api_image_server_d+"/df/items/"+self.itemId
        if "enchant" in jsonData:
            self.isenchant = True
            self.enchant = jsonData['enchant']


class WEAPON(equipment):       # 무기
    isFusion = False           # 융합이냐?
    isAsrahan = False          # 아스라한이냐?
    isCustom = False          # 불가침이냐?
    isFixed = False            # 고정픽인가?
    engraveName = False
    def initInfo(self, jsonData): # 이 json 데이터는 무기 정보만 아래 칭호와 방어구도 그에 따른 json 넘겨주기
        self.initEqInfo(jsonData)
        self.isFusion = False
        self.isAsrahan = False
        self.isCustom = False
        self.engraveName = False
        if "fusionOption" in jsonData:
            self.isFusion = True
            self.fusionOption = jsonData['fusionOption']    # 융합 옵션
            self.upgradeInfo = jsonData['upgradeInfo']      # 융합 장비 Id 및 이름
        elif "asrahanOption" in jsonData:
            self.isAsrahan = True
            self.asrahanOption = jsonData['asrahanOption']
        if "customOption" in jsonData:
            self.isCustom = True
            self.customOption = jsonData['customOption']
        elif "fixedOption" in jsonData:
            self.isFixed = True
            self.fixedOption = jsonData['fixedOption']
        if "engraveName" in jsonData:
            self.engraveName = True




class TITLE(equipment):
    def initInfo(self, jsonData):
        self.initEqInfo(jsonData)

class DEFENSEGEAR(equipment):   # 무기 이외의 장비들
    isMistGear = False
    isFixed = False
    isCustom = False
    isFusion = False
    def initInfo(self, jsonData):
        self.initEqInfo(jsonData)
        if "fusionOption" in jsonData:
            self.isFusion = True
            self.fusionOption = jsonData['fusionOption']
            self.upgradeInfo = jsonData['upgradeInfo']
        if "customOption" in jsonData:
            self.isCustom = True
            self.customOption = jsonData['customOption']
        if "fixedOption" in jsonData:
            self.isFixed = True
            self.fixedOption = jsonData['fixedOption']
        if "mistGear" in jsonData or "pureMistGear" in jsonData or "refinedMistGear" in jsonData:
            self.isMistGear = True


    
    
class PlayerInformation:
    def __init__(self):     # 저장할 클래스 준비
        self.m_equipment = [WEAPON(), TITLE()]
        for _ in range(12):
            self.m_equipment.append(DEFENSEGEAR())
        
    def initBasicInfo(self, jsonData): # 기본 정보들 초기화
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

        self.smallurl = "https://" + api_image_server_d + "/df/servers/" + self.serverId + "/characters/" + self.characterId + "?zoom=1"


    def initAdvancedInfo(self):
        #장비 정보 받기
        conn = http.client.HTTPSConnection(api_server_d)
        conn.request("GET", "/df/servers/"+self.serverId+"/characters/"+self.characterId+"/equip/equipment?apikey="+service_key_d)
        result = conn.getresponse().read().decode('utf-8')
        jsonData = json.loads(result)
        equimentjson = jsonData['equipment']

        for i in range(len(self.m_equipment)):      # 장착하지 않음으로 초기화(착용하지 않은 장비는 표기하면 안된다)
            self.m_equipment[i].isequip = False

        for i in range(len(equimentjson)):
            self.m_equipment[equipmentEnum[equimentjson[i]['slotId']]].initInfo(equimentjson[i])
        

