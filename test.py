from datetime import datetime
import sunVally_config as info
import datetime

resTime = datetime.datetime.strptime('06:25', '%H:%M')
resTime2 = datetime.datetime.strptime('11:40', '%H:%M')
targetTime = datetime.datetime.strptime(info.reserveTime, '%H:%M')

che = resTime - targetTime
che2 = resTime2 - targetTime
print(che)
print(che2)

if resTime <= targetTime:
    print("kkkk")
else:
    print("dddd")

# test = int(che.seconds / 60)
# if test >= 10:
#     print(test)





