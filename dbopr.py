#coding=gbk
from  google.appengine.ext.db import *
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from traceback import format_exc
import os, database
from igaelib import *
import igaelib
import dbsql

READPERMISSION = 0
MODIFYPERMISSION = 1

def req2ins(request):
    fieldkv = {}
    tabname = ""
    for key in request.arguments():
        value = request.get(key)
        if key == "tablename":
            tabname = value
            continue
        elif key == "operator":
            oper = request.get(key)
            continue
        elif key == 'id':
            keyid = request.get('id')
            continue
        fieldkv[key] = value
    if not tabname:
        raise Exception("No Tablename")

    dbcls = getattr(database, tabname)
    for key in fieldkv:
        clsobj = getattr(dbcls, key)
        if type(clsobj) is db.IntegerProperty and fieldkv[key]:
            fieldkv[key] = int(fieldkv[key])    
        elif type(clsobj) is db.FloatProperty:
            fieldkv[key] = float(fieldkv[key])    
    if oper == 'add':
        dbins = apply(dbcls, [], fieldkv)
        dbins.put()
    elif oper == 'modify':
        dbins = dbcls.get_by_id(int(keyid))
        for key in fieldkv:
            setattr(dbins, key, fieldkv[key])
        dbins.put()

def checkPerm(flag):
    user = str(users.get_current_user())
    try:
        chkinfo = igaelib.GetGaeVal('admindb', 'users')[0]
    except:
        return
    if chkinfo.val == 'N':
        return
    try:
        dbadmusrs = [str(e.val) for e in igaelib.GetGaeVal('admindb', 'users')]
    except:
        dbadmusrs = []
    for e in dbadmusrs:
        try:
            usr, perm = e.split('|')
        except:
            raise Exception('Error Permision Config')
        if cmp(usr, user) == 0:
            if perm[flag] == '1':
                return
    else:
        raise Exception('No Authority')

class TableOpr(webapp.RequestHandler):
    def get1(self, extra):
        try:
            request = igaelib.split_url(extra)
            curpage = request['curpage']
            tabname = request['tablename']
            pagenum = request['pagenum']
            sqlstmt = "select * from %s" %(request['tablename'], )
            fstpage  = "1"
            template_values = {
                    'sqlstmt' :     sqlstmt,
                    'tablename' :     tabname,
                    'operator':     'select',
                    'pageinf' : {
                        'curpage'  :   curpage,
                        'fstpage'  :   fstpage,
                        'pagenum'  :   pagenum,
                    },
                    'hashref' :     False
            }
            if 'instime' in igaelib._gettabfld(database, tabname):
                template_values['orderlst'] = 'instime'
            dbsql.page_sel(template_values, template_values)
            path = os.path.join(os.path.dirname(__file__), 'templates/table_sel.html')
            self.response.out.write(template.render(path, template_values))
        except:
            self.response.out.write(format_exc())        
    def insupd(self):
        tabname = extra['tablename']
        insid   = extra['id']
        dbcls = getattr(database, tabname)
        dbins = dbcls.get_by_id(insid)
        fields = [ (fld, dbins.fld) for fld in igaelib._gettabfld(database, tabname)]
        template_values = {
                'tablename' :     tabname,
                'operator':     'select',
                'fields'  :     fields
        }        
    @login_required
    def get(self):
        try:
            template_values = {
                'tmp_tabname' : igaelib._getdbtab(),
                'haha_lst'    : [1]  
            }
            url = self.request.url
            if url.find('tableopr?') > 0 :
                extra = url[url.find('tableopr?') + len('tableopr?'):]
                if url.find('curpage') > 0:
                    self.get1(extra)
                else:
                    self.insupd(extra)
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/dbopr.html')
                self.response.out.write(template.render(path, template_values))        
        except Exception as e:
            logging.error(format_exc())
            raise e
    def post(self):
        try:
            tabname = self.request.get("tablename")
            operator = self.request.get("operator")
            curpage = self.request.get("curpage", "1")
            pagenum = self.request.get("pagenum", "50")
            if operator != 'select':
                pass
            fstpage  =  "1"
            fields = igaelib._gettabfld(database, tabname)
            sqlstmt = "select * from %s " % tabname
#begin 权限控制
            global READPERMISSION, MODIFYPERMISSION
            if operator in ('select'):
                checkPerm(READPERMISSION)
                pass
            elif operator not in ('back'):
                checkPerm(MODIFYPERMISSION)
                pass
#end                
            if operator == 'clear':
                query = GqlQuery(sqlstmt)
                for result in query:
                    result.delete()
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                                    'pagenum=%s' % pagenum])
                self.get1(extra)
            elif operator == 'select':
                template_values = {
                        'sqlstmt' :     sqlstmt,
                        'tablename' :     tabname,
                        'operator':     operator,
                        'pageinf' : {
                            'curpage'  :   curpage,
                            'fstpage'  :   fstpage,
                            'pagenum'  :   pagenum,
                        },
                        'hashref' :     False
                }
                if 'instime' in igaelib._gettabfld(database, tabname):
                    template_values['orderlst'] = 'instime'                
                dbsql.page_sel(template_values, template_values)
                path = os.path.join(os.path.dirname(__file__), 'templates/table_sel.html')
                self.response.out.write(template.render(path, template_values))
            elif operator == 'insert':
                fields = [(fld, '') for fld in fields]
                template_values = {
                        'fields' : fields,
                        "tablename" : tabname,
                        "operator"  : operator,
                        }
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))
#############################################################
            elif operator == 'update':
                tabname = self.request.get('tablename')
                insid   = self.request.get('id')
                dbcls = getattr(database, tabname)
                dbins = dbcls.get_by_id(int(insid))
                fields = [ (fld, getattr(dbins, fld)) for fld in igaelib._gettabfld(database, tabname)]
#modify for update, need keyid                
                fields.append(('id', dbins.key().id()))
#end                
                template_values = {
                        'tablename' :     tabname,
                        'operator':     'add',
                        'id'      :     str(insid),
                        'fields'  :     fields
                }                        
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))
            elif operator == 'delete':
                tabname = self.request.get('tablename')
                dbcls = getattr(database, tabname)
                for keyid in self.request.get_all('id'):
                    keyid = int(keyid)
                    dbins = dbcls.get_by_id(keyid)
                    dbins.delete()
                #self.redirect('tableopr')
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                                    'pagenum=%s' % pagenum])
                self.get1(extra)
            elif operator == 'back':
                self.redirect('tableopr')
            elif operator == 'new':
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))                
##########################################################
            elif operator == 'add':
                req2ins(self.request)
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                     'pagenum=%s' % pagenum])
                self.get1(extra)                
            elif operator == 'modify':
                req2ins(self.request)
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                    'pagenum=%s' % pagenum])
                self.get1(extra)                                
        except Exception as e:
            #logging.error(format_exc())
            raise e


class TblOpr(webapp.RequestHandler):
    def get1(self, extra):
        try:
            request = igaelib.split_url(extra)
            curpage = request['curpage']
            tabname = request['tablename']
            pagenum = request['pagenum']
            sqlstmt = "select * from %s" %(request['tablename'], )
            fstpage  = "1"
            template_values = {
                    'sqlstmt' :     sqlstmt,
                    'tablename' :     tabname,
                    'operator':     'select',
                    'pageinf' : {
                        'curpage'  :   curpage,
                        'fstpage'  :   fstpage,
                        'pagenum'  :   pagenum,
                    },
                    'hashref' :     False
            }
            if 'instime' in igaelib._gettabfld(database, tabname):
                template_values['orderlst'] = 'instime'
            dbsql.page_sel(template_values, template_values)
            path = os.path.join(os.path.dirname(__file__), 'templates/table_sel.html')
            self.response.out.write(template.render(path, template_values))
        except:
            self.response.out.write(format_exc())        
    def insupd(self):
        tabname = extra['tablename']
        insid   = extra['id']
        dbcls = getattr(database, tabname)
        dbins = dbcls.get_by_id(insid)
        fields = [ (fld, dbins.fld) for fld in igaelib._gettabfld(database, tabname)]
        template_values = {
                'tablename' :     tabname,
                'operator':     'select',
                'fields'  :     fields
        }        
    def get(self):
        try:
            #user = users.get_current_user()
            #try:
            #    dbadmusrs = igaelib.GetGaeCfg('admindb', 'users').split('|')
            #except:
            #    dbadmusrs = []
            #if unicode(user) not in dbadmusrs:
            #    raise Exception('No authority')
            template_values = {
                'tmp_tabname' : igaelib._getdbtab(),
                'haha_lst'    : [1]  
            }
            url = self.request.url
            if url.find('tableopr?') > 0 :
                extra = url[url.find('tableopr?') + len('tableopr?'):]
                if url.find('curpage') > 0:
                    self.get1(extra)
                else:
                    self.insupd(extra)
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/dbopr.html')
                self.response.out.write(template.render(path, template_values))        
        except Exception as e:
            logging.error(format_exc())
            raise e
    def post(self):
        try:
            tabname = self.request.get("tablename")
            operator = self.request.get("operator")
            curpage = self.request.get("curpage", "1")
            pagenum = self.request.get("pagenum", "50")
            if operator != 'select':
                pass
            fstpage  =  "1"
            fields = igaelib._gettabfld(database, tabname)
            sqlstmt = "select * from %s " % tabname
            if operator == 'clear':
                query = GqlQuery(sqlstmt)
                for result in query:
                    result.delete()
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                                    'pagenum=%s' % pagenum])
                self.get1(extra)
            elif operator == 'select':
                template_values = {
                        'sqlstmt' :     sqlstmt,
                        'tablename' :     tabname,
                        'operator':     operator,
                        'pageinf' : {
                            'curpage'  :   curpage,
                            'fstpage'  :   fstpage,
                            'pagenum'  :   pagenum,
                        },
                        'hashref' :     False
                }
                if 'instime' in igaelib._gettabfld(database, tabname):
                    template_values['orderlst'] = 'instime'                
                dbsql.page_sel(template_values, template_values)
                path = os.path.join(os.path.dirname(__file__), 'templates/table_sel.html')
                self.response.out.write(template.render(path, template_values))
            elif operator == 'insert':
                fields = [(fld, '') for fld in fields]
                template_values = {
                        'fields' : fields,
                        "tablename" : tabname,
                        "operator"  : operator,
                        }
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))
#############################################################
            elif operator == 'update':
                tabname = self.request.get('tablename')
                insid   = self.request.get('id')
                dbcls = getattr(database, tabname)
                dbins = dbcls.get_by_id(int(insid))
                fields = [ (fld, getattr(dbins, fld)) for fld in igaelib._gettabfld(database, tabname)]
                template_values = {
                        'tablename' :     tabname,
                        'operator':     'add',
                        'id'      :     str(insid),
                        'fields'  :     fields
                }                        
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))
            elif operator == 'delete':
                tabname = self.request.get('tablename')
                dbcls = getattr(database, tabname)
                for keyid in self.request.get_all('id'):
                    keyid = int(keyid)
                    dbins = dbcls.get_by_id(keyid)
                    dbins.delete()
                #self.redirect('tableopr')
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                    'pagenum=%s' % pagenum])
                self.get1(extra)
            elif operator == 'back':
                self.redirect('tableopr')
            elif operator == 'new':
                path = os.path.join(os.path.dirname(__file__), 'templates/table_add.html')
                self.response.out.write(template.render(path, template_values))                
##########################################################
            elif operator == 'add':
                req2ins(self.request)
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                    'pagenum=%s' % pagenum])
                self.get1(extra)                
            elif operator == 'modify':
                req2ins(self.request)
                extra = '&'.join(['tablename=%s' % tabname, 'curpage=%s' % curpage, 
                                    'pagenum=%s' % pagenum])
                self.get1(extra)                                
        except Exception as e:
            logging.error(format_exc())
            raise e




