from google.appengine.ext import db

#class _BaseModel(db.Model):
#    def __init__(self):
#        super(_BaseModel, self).__init__(self)
#        _BaseModel._timeoper = db.StringProperty(time.strftime('%m%d%H%M%S'))

class GaeProjCfg(db.Model):
    proj    = db.StringProperty()
    item     = db.StringProperty()
    val   = db.StringProperty()

class GaeProjVal(db.Model):
    proj    = db.StringProperty()
    item     = db.StringProperty()
    val   = db.StringProperty()    

class Log2Db(db.Model):
    file      = db.StringProperty()
    level     = db.IntegerProperty()
    line      = db.StringProperty()
    text    = db.TextProperty()

class Weather(db.Model):
    city     =  db.StringProperty()
    temp  =     db.StringProperty()
    weath =     db.StringProperty()
    wind  =     db.StringProperty()
    cloth =     db.StringProperty()
    zwx   =     db.StringProperty()
    date  =     db.StringProperty()

class  NoteBook(db.Model):
    title = db.StringProperty()
    url = db.StringProperty()
    content = db.TextProperty()

class AcGirls(db.Model):
    sad = db.StringProperty(str)
    happy = db.StringProperty(str)

class ClearRule(db.Model):
    ruleid = db.IntegerProperty()
    tabname = db.StringProperty()
    datefld = db.StringProperty()
    condtion = db.StringProperty()
    reservedays = db.IntegerProperty()
