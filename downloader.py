#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import math
import json
from datetime import datetime
import time
import httplib
import urllib
import urlparse
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 

def request(url, cookie=''):
    ret = urlparse.urlparse(url)    # Parse input URL
    if ret.scheme == 'http':
        conn = httplib.HTTPConnection(ret.netloc)
    elif ret.scheme == 'https':
        conn = httplib.HTTPSConnection(ret.netloc)
        
    url = ret.path
    if ret.query: url += '?' + ret.query
    if ret.fragment: url += '#' + ret.fragment
    if not url: url = '/'
    
    conn.request(method='GET', url=url , headers={'Cookie': cookie})
    return conn.getresponse()

def download():
    df_names = ["min.csv","hour.csv","day.csv","week.csv"]
    dfs = []
    for df_name in df_names:
        try:
            df = pd.read_csv(df_name)
            dfs.append(df)
        except Exception, e:
            print e
            df = pd.DataFrame()
            dfs.append(df)

    now = time.localtime()
    year = str(now.tm_year)
    url = "http://ifzq.gtimg.cn/appstock/app/HotStock/getHotRankIndex"
    data = request(url)
    jsonObj = json.loads(data.read())
    if jsonObj["code"] == 0:
        dataObj = jsonObj["data"]
        minObj = dataObj["5minutes"]
        hourObj = dataObj["1hour"]
        dayObj = dataObj["1day"]
        weekObj = dataObj["1week"]
        objs = [minObj,hourObj,dayObj,weekObj]
        for i in range(0,len(objs)):
            obj = objs[i]
            df = dfs[i]
            df_name = df_names[i]
            timeStr = year + "-" + obj["rankTime"]
            print timeStr
            item_df = pd.DataFrame(obj["rankResult"])
            print item_df
            item_df["time"] = timeStr
            df = df.append(item_df)
            df.to_csv(df_name)
    else:
        print jsonObj["msg"]

if __name__ == '__main__':
    download()