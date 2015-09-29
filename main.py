# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from google.appengine.ext.webapp import util
import webapp2
from jobcron import *
from publichandler import *
from appfunc import *


app = webapp2.WSGIApplication([
    (r'/cron/zhihuribao$', ZhihuRibao),
    (r'/service/batchsendmail$', BatchSendMail),
    (r'/datastore/(\w+)$', DataStore),
    (r'/test$', Test),

],
    debug=True)


def main():
    util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
