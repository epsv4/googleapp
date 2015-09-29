#coding=gbk
import time
import traceback

from google.appengine.api import taskqueue
from google.appengine.ext import webapp

from igaelib import logging


class QueueHandler(webapp.RequestHandler):
    def get(self):
        #self.response.out.write("<html>%s</html>", %(Counter.all()))
        try:
            now = time.strftime('%Y%m%d%H%M%S')
            #queueinf = database.QueueInf(txtdesc = now)
            #queueinf.put()
            if 0:
                taskqueue.add(url='/queue1', params={'timestamp': time.strftime('%Y%m%d%H%M%S') })
            else:
                taskq = taskqueue.Queue('queue1')
                task  = taskqueue.Task(url='/queue1', params={'timestamp': time.strftime('%Y%m%d%H%M%S')})
                taskq.add(task)
            self.response.out.write('add Q succ')
        except:
             self.response.out.write(traceback.format_exc())

    def post(self):
        try:
            return self.response.set_status(301)
        except:
            logging.error(traceback.format_exc())

class Queue1Worker(webapp.RequestHandler):
    def post(self): # should run at most 1/s
        try:
            #def txn():
            #    timestamp = self.request.get('timestamp')
            #    queueinf = database.QueueInf(txtdesc = timestamp, instime = time.strftime('%Y%m%d%H%M%S'))
            #    queueinf.put()
            #db.run_in_transaction(txn)
            pass
        except:
            logging.debug(traceback.format_exc())        
        
