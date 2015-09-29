# coding=utf-8
import time, sys, os
import database
from google.appengine.ext import db
from google.appengine.ext.webapp import template

LDEBUG = 1
LINFO = 3
LERROR = 5

adminusr = 'asdseal'

def hosttype():
    if os.getcwd()[1] == ':':
        return 'w'
    else:
        return 'u'

if hosttype() == 'w':
    class logging():
        @staticmethod
        def info(s):
            _log2db(LINFO, s)
        @staticmethod
        def debug(s):
            _log2db(LDEBUG, s)
        @staticmethod
        def error(s):
            _log2db(LERROR, s)
    def _log2db(level, msg):
        frame = sys._getframe(2)
        line_no, file_name = frame.f_lineno, frame.f_code.co_filename
        loginf = database.Log2Db(text = msg, file = file_name, line = str(line_no),
                instime = time.strftime('%y%m%d%H%M%S'), level = level)
        loginf.put()
else:
    import logging

def _proxy_open(url, proxy_url='20.1.88.250',port=909):
    import urllib2
    from traceback import format_exc
    try:
        proxy=urllib2.ProxyHandler({"http":"http://%s:%s"
                %(proxy_url, port)})
        opener=urllib2.build_opener(proxy,urllib2.HTTPHandler)
        f = opener.open(url)
        return f.read()
    except Exception as e:
        logging.error(format_exc())
        return ''    

def unit_open(netType, url):
    from google.appengine.api.urlfetch  import fetch
    out = ""
    if netType == 'i':
        out = _proxy_open(url) 
    else: 
        out = fetch(url)
    return out

def split_url(url):
    rsp = {}
    kv_lst = url.split('&')
    for kv in kv_lst:
        key, value = kv.split('=')
        rsp[key] = value
    return rsp

def _getdbtab():
    import database, types
    tables = []
    for x in dir(database):
        try:
            if issubclass(getattr(database, x), db.Model):
                tables.append(x)
        except:
            pass
    tables.sort()
    return tables

def _gettabfld(module, tabname):
    tabcls = getattr(module, tabname)
    return tabcls.properties().keys()

def GeneralError(self, req):
    path = os.path.join(os.path.dirname(__file__), 'templates/response_err.html')
    self.response.out.write(template.render(path, req))     

def GetGaeCfg(proj, key):
    retvals = db.GqlQuery('select * from GaeProjCfg where proj = :1', proj)
    for val in retvals:
        if key == val.item:
            return val.val
    return None

def GetGaeVal(proj, key):
    retvals = db.GqlQuery('select * from GaeProjVal where proj = :1', proj)
    vals = []
    if key is None:
        return retvals
    for val in retvals:
        if key == val.item:
            vals.append(val)
    return vals
