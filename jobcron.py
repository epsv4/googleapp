# coding=utf-8
import traceback
import urllib2
from google.appengine.api.taskqueue import taskqueue
import webapp2
from weather import weather
from google.appengine.api import mail
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db
from traceback import format_exc
import datetime, time
import igaelib
import models
from google.appengine.ext.db import GqlQuery
from BeautifulSoup import BeautifulSoup
from igaelib import logging


class CronWeather(webapp2.RequestHandler):
    def get(self):
        try:
            today = time.strftime('%Y%m%d')
            citycode = igaelib.GetGaeCfg('weather', 'city')
            mail.send_mail(sender='asdseal@gmail.com', to='18221655453@139.com', subject='%s' % '天气',
                           body=weather(citycode))
        except Exception as e:
            logging.error(format_exc())
            raise e


class CronClock(webapp2.RequestHandler):
    def get(self):
        pass


class CronClrHis(webapp2.RequestHandler):
    @login_required
    def get(self):
        sqlstmt = 'select * from ClearRule'
        clearrule = db.GqlQuery(sqlstmt)
        for rule in clearrule:
            logging.debug(rule.tabname)
            today = datetime.date.today()
            whenday = today - datetime.timedelta(rule.reservedays)
            sqlstmt = 'select * from %s where %s <= %s and %s' \
                      % (rule.tabname, rule.datefld, whenday.strftime('%y%m%d%H%M%S'), rule.condtion)
            query = db.GqlQuery(sqlstmt)
            for result in query:
                result.delete()


# 获取知乎日报
class ZhihuRibao(webapp2.RequestHandler):
    def getPosts(self, url):
        html = self.getHtml(url)
        result = {}
        soup = BeautifulSoup(html.decode('utf-8'))
        posts = soup.findAll('div', {'class': 'post'})
        for post in posts:
            postdate = post.find('span', {'class': 'dateString'}).contents[0][:10]
            items_l = []
            for item in post.findAll('div', {'class': 'item'}):
                item_m = dict()
                href = dict(item.a.attrs)['href']
                title = str(item.a.span.contents[0]).decode('utf-8')
                image = dict(item.a.img.attrs)['src']
                item_m['href'] = href
                item_m['title'] = title
                item_m['image'] = image
                items_l.append(item_m)
            result[postdate] = items_l
        return result

    def getHtml(self, url):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                  'Referer': '******'}
        request = urllib2.Request(url, None, header)
        response = urllib2.urlopen(request)
        text = response.read()
        return text

    @login_required
    def get(self):
        try:
            t = time.strftime("%Y%m%d%H%M%S")
            date, tm = t[:8], t[8:]
            count = 0
            posts = self.getPosts('http://zhihudaily.ahorn.me')
            for postdate in posts.keys():
                for item in posts[postdate]:
                    sql = "select * from zhihuribao where href = '%s'" % (item['href'])
                    query = GqlQuery(sql)
                    new = True
                    for q in query:
                        new = False
                    if new:
                        zhihu = models.zhihuribao(date=postdate, img=item['image'], href=item['href'],
                                                  title=item['title'], insdate=date)
                        zhihu.put()
                        count += 1
            if count >= 0:
                taskq = taskqueue.Queue('queue1')
                task  = taskqueue.Task(url='/service/batchsendmail', params={'insdate': date, 'kind': 'zhihuribao'})
                taskq.add(task)
            self.response.out.write("Succ")
        except Exception as e:
            logging.error(traceback.format_exc())
