from google.appengine.ext import db
import database
import igaelib
from igaelib import *

def page_sel(req, rsp):
    sqlstmt = req['sqlstmt']
    if 'orderlst' in req:
        sqlstmt = '%s order by %s' %(sqlstmt, req['orderlst'])
    pagenum = int(req['pageinf']['pagenum'])
    curpage = int(req['pageinf']['curpage'])
    operator = req['operator']
    tabname = req['tablename']
    query = db.GqlQuery(sqlstmt)
    rtntotal = query.count()
    pageidx = (curpage  - 1) * pagenum
    fields = igaelib._gettabfld(database, tabname)
    values = []
    raw_values = query.fetch(pagenum, pageidx)
    if req.get('hashref', False):
        pass
    else:
        pass
    for x, v in enumerate(raw_values):
        tmp = []
        tmp.append(str(x + 1))
        tmp.append(v.key().id())
        for fld in fields:
            tmp.append(getattr(v, fld))
        insid = v.key().id()
        values.append((insid, tmp))
    rsp['values'] = values
    rsp['fields'] = fields
    rsp['tablename'] = tabname
    shang, yushu = divmod(rtntotal, pagenum) 
    rsp['pageinf']['rtntotal'] = str(rtntotal)
    rsp['pageinf']['pagecount'] = str(shang + 1 if yushu else shang)
    rsp['pages'] = []
    for idx in xrange(int(rsp['pageinf']['pagecount'])):
        rsp['pages'].append((str(idx + 1), 'tableopr?tablename=%s&operator=%s&curpage=%s&pagenum=%d' \
            %(tabname, operator, idx + 1, pagenum)))
