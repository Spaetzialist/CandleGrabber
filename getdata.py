from time import sleep

import requests
import os
import pickle
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)
NumOfDays = 7


def millis(t):
    return int((t - epoch).total_seconds() * 1000)


if os.path.isfile("data"):
    with open("data", "rb") as fp:
        out = pickle.load(fp)
        start = out[-1][0]
else:
    out = []

    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=NumOfDays)
    sdate = datetime.datetime(week_ago.year, week_ago.month, week_ago.day, 0, 0)
    start = millis(sdate)

minute = 60 * 1000
now = millis(datetime.datetime.now())
baseurl = 'https://api.bitfinex.com/v2/candles/'
timeframe = '1D'
symbol = ['tBCHUSD','tEOSUSD','tREPUSD','tXRPUSD','tDSHUSD','tZECUSD','tXRPUSD','tXLMUSD','tLTCUSD','tXMRUSD','tBTCUSD','tETCUSD','tETHUSD']
d= {}
errorList=[]

sleeptime = 1

def getRes(start,s):
    end = start + minute * 1001
    url = "%strade:%s:%s/hist?start=%s&end=%s&limit=1000" % (baseurl, timeframe, s, str(start), str(end))
    return requests.get(url)

for s in symbol:
    while now > (start + minute * 1000):
        res = getRes(start,s)
        #print(str(datetime.datetime.fromtimestamp(start / 1000)) + " code: " + str(res.status_code))
        if res.status_code == 200:
            out += list(reversed(res.json()))
            start += minute * 1000
            sleep(sleeptime)
        else:
            sleep(10)

    #print("Test sanity")
    timestamp = out[0][0]
    #print("first: %d", timestamp)

    minList=[]
    maxList=[]
    for l in out:
        #if not l[0] == timestamp + 1000 * 60:
            #print(l, timestamp, l[0] - timestamp)
        #print (str(datetime.datetime.fromtimestamp(l[0] / 1000)))
        timestamp = l[0]
        minList.append(l[4])
        maxList.append(l[3])
    #---------Ausgabe---------


    if (len(out)!=NumOfDays):
        errorList.append ("Error at " + s + ". Only " + str(len(out)) + " elements loaded")
    DClow=min(minList)
    DChigh=max(maxList)
    calc = round((1-DClow/DChigh)*100,1)
    d[s]=calc
    print (s + " (" + str(len(out)) + "): " + str(calc)+"%")
    #print (str(datetime.datetime.fromtimestamp(out[0][0] / 1000)))
    #print (str(datetime.datetime.fromtimestamp(out[len(out)-1][0] / 1000)))
    #print ("Min = " + str(min(minList)))
    #print ("Max = " + str(max(maxList)))

    start = millis(sdate)
    out = []
print ("## Result ##")
l = (sorted(d, key=d.get))
for e in l:
    print (e[1:4] + ": " +str(d[e])+"%")
for e in errorList:
    print (e)
    #with open('data', 'wb') as fp:
    #    pickle.dump(out, fp)

#todo:
#Ergebnis in Datei schreiben
#DC 3 und Entfernung davon mit reinnehmen