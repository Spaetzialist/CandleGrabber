from time import sleep

import requests
import os
import pickle
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def millis(t):
    return int((t - epoch).total_seconds() * 1000)


if os.path.isfile("data"):
    with open("data", "rb") as fp:
        out = pickle.load(fp)
        start = out[-1][0]
else:
    out = []

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    sdate = datetime.datetime(week_ago.year, week_ago.month, week_ago.day, 0, 0)
    start = millis(sdate)

minute = 60 * 1000
now = millis(datetime.datetime.now())
baseurl = 'https://api.bitfinex.com/v2/candles/'
timeframe = '1d'
symbol = 'tBTCUSD'


sleeptime = 1

def getRes(start):
    end = start + minute * 1001
    url = "%strade:%s:%s/hist?start=%s&end=%s&limit=1000" % (baseurl, timeframe, symbol, str(start), str(end))
    return requests.get(url)


while now > (start + minute * 1000):
    res = getRes(start)
    print(str(datetime.datetime.fromtimestamp(start / 1000)) + " code: " + str(res.status_code))
    if res.status_code == 200:
        out += list(reversed(res.json()))
        start += minute * 1000
        sleep(sleeptime)
    else:
        sleep(10)

print("Test sanity")
timestamp = out[0][0]
print("first: %d", timestamp)

for l in out:
    #if not l[0] == timestamp + 1000 * 60:
        #print(l, timestamp, l[0] - timestamp)
    print (str(datetime.datetime.fromtimestamp(l[0] / 1000)))
    timestamp = l[0]
print ("----")
print (str(datetime.datetime.fromtimestamp(out[0][0] / 1000)))
print (str(datetime.datetime.fromtimestamp(out[len(out)-1][0] / 1000)))
print ("out len = " + str(len(out)))
with open('data', 'wb') as fp:
    pickle.dump(out, fp)
