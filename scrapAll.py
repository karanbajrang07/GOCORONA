import os
import numpy as np
import re
import pandas as pd
import urllib.request
import time

dates = ['30-01-2020', '31-01-2020']

for i in range(29):
    date = i + 1
    tempDate = str(date) + "-02-2020"
    dates.append(tempDate)

for i in range(22):
    date = i + 1
    tempDate = str(date) + "-03-2020"
    dates.append(tempDate)

# print(dates)

fullData = []

for date in dates:
    time.sleep(1 + np.random.random())
    tempUrl = "https://covidout.in/?start=" + str(date) + "&end=" + str(date)
    print(tempUrl)

    htmlText = ""
    with urllib.request.urlopen(tempUrl) as url:
        htmlText = url.read()
        htmlText = htmlText.decode('ISO-8859-1')
        these_regex = "number-graph-wrapper\"(.+?)<div class=\"columns"
        pattern = re.compile(these_regex)
        singleData = re.findall(pattern, htmlText)

        these_regex2 = "case\">(.+?)<"
        pattern2 = re.compile(these_regex2)
        tempArr = re.findall(pattern2, singleData[0])
        fullData.append(tempArr)

print(fullData)