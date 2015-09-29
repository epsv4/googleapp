from google.appengine.ext import db


class keyvalue(db.Model):
    _field = ('key1', 'value1')
    key1 = db.StringProperty()
    value1 = db.StringProperty()


class zhihuribao(db.Model):
    _field = ('date', 'img', 'href', 'title', 'reserve1', 'reserve2', 'insdate')
    date = db.StringProperty()
    img = db.StringProperty()
    href = db.StringProperty()
    title = db.StringProperty()
    insdate = db.StringProperty()
    reserve1 = db.StringProperty()
    reserve2 = db.StringProperty()

class subscription(db.Model):
    _field = ('rssid', 'email', 'status', 'reserve1', 'reserve2')
    rssid = db.StringProperty()
    email = db.StringProperty()
    status = db.StringProperty()
    reserve1 = db.StringProperty()
    reserve2 = db.StringProperty()


class rssstore(db.Model):
    _field = ('rssid', 'rss', 'date', 'time' 'reserve1', 'reserve2')
    rssid = db.StringProperty()
    rss = db.StringProperty()
    date = db.StringProperty()
    time = db.StringProperty()
    reserve1 = db.StringProperty()
    reserve2 = db.StringProperty()

class dumplicate(db.Model):
    _field = ('app', 'duplicate', 'date')
    app = db.StringProperty()
    duplicate = db.StringProperty()
    date = db.StringProperty()

class generalstore(db.Model):
    key1 = db.StringProperty()
    key2 = db.StringProperty()
    key3 = db.StringProperty()
    key4 = db.StringProperty()
    key5 = db.StringProperty()
    key6 = db.StringProperty()
    value1 = db.StringProperty()
    value2 = db.StringProperty()
    value3 = db.StringProperty()
    value4 = db.StringProperty()
    value5 = db.StringProperty()
    value6 = db.StringProperty()
