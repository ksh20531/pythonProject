import sunVally_config as sunV
import ssl
import requests
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def makeTarget():
    data = {}
    now = datetime.now()
    nine = datetime(now.year, now.month, now.day, 9, 00)

    if nine > now:
        nine = datetime(now.year, now.month, now.day, 9, 30)
        data[0] = sunV.ilJuk
        data[1] = sunV.timeIljuk

        if nine > now:
            nine = datetime(now.year, now.month, now.day, 10, 30)
        data[0] = sunV.yeoJu
        data[1] = sunV.timeYeoju
    else:
        data[0] = sunV.sulAk
        data[1] = sunV.timeSulak
        return data


target = makeTarget()[0]
targetTime = datetime.strptime(makeTarget()[1], '%H:%M:%S').time()
print(type(targetTime), "targetTime :", targetTime)

# ssl 오류 발생 방지용
ssl._create_default_https_context = ssl._create_unverified_context

# 크롬 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
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
driver.find_element(By.ID, sunV.btnId + target).click()
print("move to target")

# 예약시간 timer
while True:
    date = datetime.now().strftime('%H:%M:%S')
    time = datetime.strptime(date, '%H:%M:%S').time()
    sleep(0.5)
    print('type :', type(time), "time : ", time)

    if time == targetTime:
        driver.refresh()

        # 날짜 선택
        req = requests.get(sunV.url_reservation + '?sel=' + target)
        if req.status_code == 200:
            try:
                date = "A"+sunV.reserveDate
            except:
                date = "B"+sunV.reserveDate

            print('selected date is ',date)
            driver.find_element(By.ID, date).click()
        else:
            print("date select error")

        # 시간 선택
        req2 = requests.get(sunV.url_ajax)
        print("ajax status :", req2.status_code)

        if req2.status_code == 200:
            elements = driver.find_elements(By.CSS_SELECTOR, '#tabCourseALL > div > div > table > tbody > tr')
            reserveTime = datetime.strptime(sunV.reserveTime, '%H:%M:%S')

            for e in elements:
                # 예약 시간 datetime형식으로 변환 범위 계산
                resTime = datetime.strptime(e.text.split(' ')[3], '%H:%M')
                diff = resTime - reserveTime
                diff = int(diff.seconds / 60)  # second to minute

                # 예약시간 이상이고, 범위 안에 들었을 경우
                if (resTime >= reserveTime and diff <= sunV.timeRange):
                    if e.text.find('마감') < 0:
                        e.find_element(By.CLASS_NAME, 'btn-res').click()
                        print("move to select page")
                        break
            try:
                driver.find_element(By.CLASS_NAME, 'btn-res03').click()
                print('success')
            except:
                print('fail')
                pass
        break

print("program end")
