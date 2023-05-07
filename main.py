from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import urllib.request

my_id = 51060500
my_pw = 160290

url_reservation = 'https://www.sunvalley.co.kr/reservation/golf'
url_login = 'https://www.sunvalley.co.kr/member/login'

#네이버 시계
#실시간으로 계속 받아올 수 있게 수정해야 함
naver = 'http://www.naver.com'
date = urllib.request.urlopen(naver).headers['Date'][5:-4]
hour, min, sec = date[12:14], date[15:17], date[18:]

#크롬 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

#페이지 오픈
driver.get(url_login)

#아이디,비밀번호 입력 후 로그인 클릭
driver.find_element(By.ID, "usrId").send_keys(my_id)
driver.find_element(By.ID, "usrPwd").send_keys(my_pw)
driver.find_element(By.ID, "fnLogin").click()

#alert 창 처리를 위한 sleep
sleep(1)

#alert 창처리
try:
    alert = driver.switch_to.alert.accept()
except:
    pass

#예약 페이지로 이동
driver.get(url_reservation)

#조건문
#몇시일땐 일죽 등등
