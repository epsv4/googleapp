#coding=utf-8
import json, os,  sys, urllib2
from traceback import format_exc
from igaelib import unit_open, logging
from google.appengine.api.urlfetch  import fetch

def GetJson(citycode):
    try:
        url = "http://m.weather.com.cn/data/%s.html" %(citycode,)
        data = urllib2.urlopen(url).read()
        return  json.loads(data)['weatherinfo']
    except:
        logging.error(format_exc())
        return ''

def parseJson(jsn):
    kv = {}
    kv['temp']      =   jsn['temp1'].encode('gbk')
    kv['weather']   =   jsn['weather1'].encode('gbk')
    kv['wind']      =   jsn['wind1'].encode('gbk')
    kv['cloth']     =   jsn['index48_d'].encode('gbk')
    kv['zwx']       =   jsn['index48_uv'].encode('gbk')
    return kv

def weather(citycode):
    try:
        jsn = GetJson(citycode)
        if not jsn:
            return ''
        jsn = parseJson(jsn)
        info =  "天气:%s\n温度:%s\n风力:%s\n紫外线:%s\n穿衣:%s" \
                %(jsn['weather'], jsn['temp'], jsn['wind'], jsn['zwx'], jsn['cloth'])
        return info.decode('gbk').encode('utf8')
    except Exception as e :
        logging.error(format_exc())
        return ""

if __name__ == '__main__':
    loginit('weather.log')
    print weathedatar('101020100')
