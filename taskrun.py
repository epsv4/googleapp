#coding=gbk
from igaelib import logging
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import taskqueue
from google.appengine.ext import deferred
from google.appengine.ext.webapp.util import login_required

from copy import deepcopy
import os, datetime, time, traceback, cgi

from execq import *
from jobcron import *
import database
from google.appengine.api import mail
from traceback import format_exc
from igaelib import *


class SendMail(webapp.RequestHandler):
    def get(self):
        try:
            mail.send_mail(sender='asdseal@gmail.com', to='zhou_han@shhicom.com', subject='yoo', body='haha')
            self.response.out.write('ok')
        except:
            self.response.out.write(format_exc())

class YouDao(webapp.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class SetCet6Word(webapp.RequestHandler):
    def get(self, wordtranslate):
        try:
            word, translate = wordtranslate.split('_')
            #wordtranslate = wordtranslate.decode('utf8')
            #logging.debug(str(len(wordtranslate))) 
            #logging.debug(str(wordtranslate))
            translate = unicode(translate, 'utf8')
            wordinf = database.Cet6Word(word = word, translate = translate, emerge = False, \
                    complex = None, lasttime = "")
            wordinf.put()
            self.response.out.write("OK")
        except:
            self.response.out.write(format_exc())


class SetCet6WordTerm(webapp.RequestHandler):
    def get(self, wordtranslate):
        try:
            wordtranslate = unicode(wordtranslate, 'gbk')
            word, translate = wordtranslate.split('_')
            #logging.debug(wordtranslate.count('%'))
            #wordtranslate = wordtranslate.decode('utf8')
            #logging.debug(str(len(wordtranslate))) 
            #logging.debug(str(wordtranslate))
            wordinf = database.Cet6Word(word = word, translate = translate, emerge = False, \
                    complex = None, lasttime = "")
            wordinf.put()
            self.response.out.write("OK")
        except:
            self.response.out.write(format_exc())

class GetCet6Word(webapp.RequestHandler):
    def get(self):
        try:
            outdata = ''
            query = db.GqlQuery("select * from QueueInf")
            #outdata += str(type(query))
            data = query.fetch(10)
            for d in data:
                d.delete()
            #query = database.QueueInf.all()
            #data = query.fetch(1)
            self.response.out.write("OK")
            #self.response.out.write(data[0].txtdesc)

        except:
            self.response.out.write('except')
            self.response.out.write(format_exc())

class AddNoteBook(webapp.RequestHandler):
    def get(self):
        try:
            template_values = {
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/notebook.html')
            self.response.out.write(template.render(path, template_values))                    
        except:
            logging.error(format_exc())
    def post(self):
        try:
            title = self.request.get("title")
            content = self.request.get("content")
            if not title or not content:
                GeneralError(self, {'errmsg' : 'title or content is null'})
                return
            notebook = database.NoteBook(title = title, content = content, instime = time.strftime('%y%m%d%H%M%S'))
            notebook.put()
            self.redirect('notebook')
        except:
            logging.error(format_exc())
            self.response.out.write(format_exc())
