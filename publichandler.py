# coding=utf-8
import webapp2
from google.appengine.ext.db import GqlQuery
from google.appengine.api import mail
from igaelib import logging
from traceback import format_exc


class BatchSendMail(webapp2.RequestHandler):
    def post(self):
        try:
            kind = self.request.get("kind")
            logging.debug(kind)
            if kind == "zhihuribao":
                insdate = self.request.get("insdate")
                result = GqlQuery("select * from zhihuribao where insdate = '%s'" % (insdate,))
                ribao = u"\n\n".join([u"%s\n%s" % (r.title, r.href) for r in result])
                subscribeusrs = GqlQuery("select * from subscription where rssid = 'zhihuribao'")
                for user in subscribeusrs:
                    if user.email != "":
                        logging.debug(user.email)
                        mail.send_mail(sender='asdseal@gmail.com', to=user.email, subject='知乎日报-%s' % insdate, body=ribao)
                    else:
                        logging.debug("something wrong")
            self.response.out.write("Ok")
        except:
            logging.error(format_exc())