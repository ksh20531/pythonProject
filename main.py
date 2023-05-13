import json
import sunVally_config as info
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from time import sleep
import requests
import urllib.request
import ssl
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime

# ssl 오류 발생 방지용
ssl._create_default_https_context = ssl._create_unverified_context

target = info.sulAk

# 네이버 시계
# 실시간으로 계속 받아올 수 있게 수정해야 함
naverUrl = 'http://www.naver.com'
date = urllib.request.urlopen(naverUrl).headers['Date'][5:-4]
hour, min, sec = date[12:14], date[15:17], date[18:]

# 크롬 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()  # 창 최대화 옵션
driver.implicitly_wait(10)  # 페이지 로드 시간 옵션

# 페이지 오픈
driver.get(info.url_login)

# 아이디,비밀번호 입력 후 로그인 클릭
driver.find_element(By.ID, "usrId").send_keys(info.my_id)
driver.find_element(By.ID, "usrPwd").send_keys(info.my_pw)
driver.find_element(By.ID, "fnLogin").click()

# alert 창 처리를 위한 sleep
sleep(0.5)

# alert 창처리
try:
    alert = driver.switch_to.alert
    alert.accept()
    print('alert ok')
except:
    alert = driver.switch_to.alert.dismiss()
    print('alert error')
    pass

# 테스트 필요
# Alert(driver).accept()
# Alert(driver).dismiss()
#
# print(Alert(driver).text)
# Alert(driver).send_keys(keysToSend=Keys.ESCAPE)

# 예약 페이지로 이동
driver.get(info.url_reservation)
print("move to reserve page")
driver.find_element(By.ID, info.btnId+target).click()
print("move to target")

# 정해진 시간에 새로고침 되게 수정 해야 함.


# 새로고침
# driver.refresh()

# 날짜 선택
req = requests.get(info.url_reservation+'?sel='+target)
if req.status_code == 200:
    try:
        date = "A"+info.reserveDate
    except:
        date = "B"+info.reserveDate
    print(date)
    driver.find_element(By.ID, date).click()
else:
    print("date select error")

req2 = requests.get(info.url_ajax)
print("ajax status :", req2.status_code)

if req2.status_code == 200:
    elements = driver.find_elements(By.CSS_SELECTOR, '#tabCourseALL > div > div > table > tbody > tr')
    targetTime = datetime.strptime(info.reserveTime, '%H:%M')

    for e in elements:
        # 예약 시간 datetime형식으로 변환 후 차이 계산
        resTime = datetime.strptime(e.text.split(' ')[3], '%H:%M')
        diff = resTime - targetTime
        diff = int(diff.seconds / 60)  # datetime to int

        if (resTime >= targetTime and diff <= info.timeRange):
            print(e.text)
            e.find_element(By.CLASS_NAME, 'btn-res').click()
            break

    print("move to select page")
    driver.find_element(By.CLASS_NAME, 'btn-res03').click()

print("end")
