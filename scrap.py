import os
# import urllib
import re
import pandas as pd
import urllib.request
import datetime
global str

def update_data():
    htmlText = ""
    with urllib.request.urlopen("https://www.mohfw.gov.in") as url:
        htmlText = url.read()

    htmlText = htmlText.decode('ISO-8859-1')
    htmlTextSingleLine = re.sub("\n", " ", htmlText)

    these_regex = "<tbody>(.+?)</tbody>"
    pattern = re.compile(these_regex)
    allData = re.findall(pattern, htmlTextSingleLine)

    these_regex2 = "<tr>(.+?)</tr>"
    pattern2 = re.compile(these_regex2)
    stateWiseData = re.findall(pattern2, allData[1])
    stateWiseData = stateWiseData[:-2]

    ##New data and old DF
    df = pd.read_csv("data_covid1.csv")

    intial=df.shape[0]

    ##Unique Key
    def column_key_return(data):
        x=""
        for i in data.columns[:-1]:
            x=x+"-"+data[i]
        return x

    def key_of_array(arrays):
        x=""
        for i in range(len(arrays)):
            x=x+"-"+arrays[i]
        return x



    these_regex3 = "<td.+?>(.+?)</td>"
    pattern3 = re.compile(these_regex3)
    allArr = []
    time_now= datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S:%f")
    for str in stateWiseData:
        tempArr = re.findall(pattern3, str)
        tempArr = tempArr[1:]
        key=key_of_array(tempArr)
        
        if ~df['unique_key'].str.contains(key).any():
            tempArr.append(time_now)
            tempArr.append(key)
            df=df.append(dict(zip(df.columns, tempArr)), ignore_index=True)

        allArr.append(tempArr)

    final=df.shape[0]

    df["rank"]=df.sort_values(["Name","updated_at"],ascending=False).groupby(['Name']).cumcount() + 1

    latest=df[df["rank"]==1]

    total_count = int(latest.sum()["Total Confirmed cases(Indian)"]) + int(latest.sum()["Total Confirmed cases(Foreign)"]) + int(latest.sum()["Death"]) + int(latest.sum()["Cured"])

    log="\nAt time {0} rows affected were: {1}, total cases are: {2}".format(time_now,(final-intial),total_count)

    # Open a file with access mode 'a'
    with open("scrap_log.txt", "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(log)
    print(log)
    df.to_csv("data_covid1.csv",index=False)
    return df