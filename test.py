from datetime import datetime
import sunVally_config as sunV
from time import sleep
import urllib.request
import ssl
from pytz import timezone, utc
import threading

reserveTime = datetime.strptime(sunV.reserveTime, '%H:%M:%S')  # datetime.datetime
date = datetime.now().strftime('%H:%M:%S')  # str
time = datetime.strptime(date, '%H:%M:%S').time()  # datetime.time
print(type(reserveTime), reserveTime)
print(type(date), date)
print(type(time), time)


print(type(reserveTime), reserveTime)

# resTime = datetime.strptime('11:41', '%H:%M')  # 문자열을 datetime로 변환
# diff = resTime - reserveTime
# diff = int(diff.seconds / 60)  # second to minute
#
# print(type(diff), diff)


# date = datetime.now().strftime('%H:%M:%S')
# time = datetime.strptime(date, '%H:%M:%S').time()
# print('date :', type(date), date)
# print('time :', type(time), time)
#
# test = datetime.strptime(sunV.date, '%H:%M:%S').time()
# print('test :', type(test), test)

#
#
# end = False
# while not end:
#     date = datetime.now().strftime('%H:%M:%S')
#     kkk = datetime.strptime(date, '%H:%M:%S').time()
#     sleep(0.5)
#     if kkk == test:
#         print("same")
#         break
#     else:
#         test1()
#         print(date)
# print('end')

# result = []
#
#
# def printer(message):
#     print(message)
#
#
# def tim():
#     while True:
#         time = datetime.now().time()
#         result.append(time)
#         printer(time)
#         if time == datetime.strptime(sunV.date, '%H:%M:%S').time():
#             print("same")
#             break
#         sleep(1)
#
#
# th1 = threading.Thread(target=tim, args=())
# th1.start()
#
# print('result3 :', result)
# print(result[0])
# sleep(3)
# print("sleep 3 sec")
# print(result[0])



# sleep 걸고 시간 받아오는 것 차이 확인용
# sec = datetime.now().time()
# print(sec)
# sleep(2)
# print(sec)
#
# print(datetime.now().time())
# sleep(2)
# print(datetime.now().time())


# 시간 계산
# today = datetime.now()
# test = datetime.strptime(sunV.date, '%Y-$M-%d %H:%M:%s')
# print(type(today), today)
# print(type(test), test)
# diffTime = today - test
# print(diffTime)
# end = False
# while not end:
#     today = datetime.now()
#     if today.time() >= datetime.strptime(info.timeSulak, '%H:%M'):
#         print(1)
