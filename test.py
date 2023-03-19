import time
import datetime
date = "0123"
while True:
    m = int(input())
    td = datetime.date.today()
    y = -1
    if td.month > m:
        y = td.year + 1
    else:
        y = td.year
    print(y)

#t = "7:03"
#print(list(map(int, t.split(":"))))
