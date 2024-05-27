

class PCInfo:
    def __init__(self, SIGUN_CD, SIGUN_NM, BIZPIC_NM, LICENSG_DE, LONTO, ROADNM, ZIP_CD, LAT, LOGT):
        self.SIGUN_CD = SIGUN_CD        # 시군 코드
        self.SIGUN_NM = SIGUN_NM        # 시군 이름
        self.BIZPIC_NM = BIZPIC_NM      # 기관 이름
        self.LICENSG_DE = LICENSG_DE    # 허가 날짜
        self.LONTO_ADDR = LONTO         # 지번 주소
        self.ROADNM_ADDR = ROADNM       # 도로명 주소
        self.ZIP_CD = ZIP_CD            # 우편 번호
        self.WGS_LOGT = LOGT            # WGS84 경도
        self.WGS_LAT = LAT              # WGS84 위도