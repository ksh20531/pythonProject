import sunVally_config as sunV
import ssl
import requests
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 골프장 자동 선택
def makeTarget():
    # return sunV.test
    now = datetime.now()
    first_time = datetime(now.year, now.month, now.day, 9, 00)
    second_time = datetime(now.year, now.month, now.day, 9, 30)

    if first_time > now:
        return sunV.sulAk
    elif first_time < now < second_time:
        return sunV.ilJuk
    elif second_time < now:
        return sunV.yeoJu
    else:
        return sunV.test


makeTarget = makeTarget()
target = makeTarget['code']
startTime = datetime.strptime(str(datetime.now().date()) + " " + makeTarget['time'], '%Y-%m-%d %H:%M:%S')
targetDatetime = datetime.strptime(makeTarget['reserveDatetime'], '%Y-%m-%d %H:%M:%S')
print(makeTarget)

if targetDatetime.month == datetime.now().month:
    selectedDate = "A" + format(targetDatetime.year, '04') + format(targetDatetime.month, '02') + format(targetDatetime.day, '02')
else:
    selectedDate = "B" + format(targetDatetime.year, '04') + format(targetDatetime.month, '02') + format(targetDatetime.day, '02')

# ssl 오류 발생 방지용
ssl._create_default_https_context = ssl._create_unverified_context

# 크롬 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
try:
    # https://chromedriver.chromium.org/downloads
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
except:
    webbrowser.open("https://googlechromelabs.github.io/chrome-for-testing/")
    path = os.getcwd()
    print(path)
    os.startfile(path)
    # driver = webdriver.Chrome(path+'/chromedriver.exe', options=chrome_options)
    exit()

driver.maximize_window()  # 창 최대화 옵션
driver.implicitly_wait(10)  # 페이지 로드 시간 옵션

# 페이지 오픈
driver.get(sunV.url_login)

# 아이디,비밀번호 입력 후 로그인 클릭
driver.find_element(By.ID, "usrId").send_keys(sunV.my_id)
driver.find_element(By.ID, "usrPwd").send_keys(sunV.my_pw)
driver.find_element(By.ID, "fnLogin").click()

# alert 창 처리를 위한 sleep
# sleep(0.5)

# alert 창처리
try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print('alert ok')
except:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.dismiss()
    print('alert error')
    pass


# 예약 페이지로 이동
driver.get(sunV.url_reservation)
print("move to reserve page")
driver.find_element(By.ID, 'selectCoId' + target).click()
print("move to target")

# 예약시간 timer
timeRange = sunV.timeRange
reserveTime = datetime.strptime(makeTarget['reserveDatetime'], '%Y-%m-%d %H:%M:%S')  # datetime.datetime

while True:
    start = (startTime - datetime.now()).total_seconds()
    if start < 0.2:
        driver.refresh()
        print('----------start----------')
        # 날짜 선택
        req = requests.get(sunV.url_reservation + '?sel=' + target)
        if req.status_code == 200:
            driver.find_element(By.ID, selectedDate).click()
            print('selected date is ', selectedDate)
        else:
            print("date select error")
            break

        # 시간 선택
        req2 = requests.get(sunV.url_ajax)
        print("ajax status :", req2.status_code)

        if req2.status_code == 200:
            elements = driver.find_elements(By.CSS_SELECTOR, '#tabCourseALL > div > div > table > tbody > tr')

            for e in elements:
                # 예약 시간 datetime형식으로 변환 범위 계산
                if e.text.find('마감') < 0:
                    targetTime = datetime.strptime(str(reserveTime.date()) + ' ' + e.text.split(' ')[3], '%Y-%m-%d %H:%M')
                    diff = targetTime - reserveTime  # second
                    diff = int(diff.seconds / 60)  # second to minute
                    # 예약시간 이상이고, 범위 안에 들었을 경우
                    if (targetTime >= reserveTime and diff <= timeRange):
                        e.find_element(By.CLASS_NAME, 'btn-res').click()
                        print("move to select page")
                        break

                    else:
                        print("is booked")
            try:
                driver.find_element(By.CLASS_NAME, 'btn-res03').click()
                print('성공')
                break
            except:
                print('동시 예약')
            break
        else:
            print('communication error')

print("program end")
