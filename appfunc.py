# coding=utf-8
import webapp2
from google.appengine.ext.db import GqlQuery
from google.appengine.api import mail
from igaelib import logging
from traceback import format_exc
from google.appengine.ext.webapp.util import login_required
import models
import initialize

templateenv = initialize.templateenv


class DataStore(webapp2.RequestHandler):
    @login_required
    def get(self, table):
        try:
            clazz = getattr(models, table)
            fields = getattr(clazz, '_field')
            rspdict = {}
            rspdict['fieldsdef'] = fields
            rspdict['table'] = table
            template = templateenv.get_template("app/datastore.get.html")
            self.response.out.write(template.render(rspdict))
        except:
            logging.error(format_exc())

    def post(self, table):
        try:
            operateflag = self.request.get('operateflag')
            clazz = getattr(models, table)
            fields = getattr(clazz, '_field')
            if operateflag == 'I':
                d = dict([(field, self.request.get(field)) for field in fields])
                q = clazz.all()
                for key in d.keys():
                    q = q.filter('%s =' % key, d[key])
                e = None
                for i in q:
                    e = i
                if not e:
                    e = apply(clazz, [], d)
                    e.put()
                else:
                    for key in d.keys():
                        setattr(e, key, d[key])
                    e.put()
        except Exception as e:
            logging.error(format_exc())
        finally:
            self.redirect("/datastore/%s" % table)

class Test(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("哈哈")