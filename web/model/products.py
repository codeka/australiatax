
from google.appengine.ext import db


class Company(db.Model):
  name = db.StringProperty()
  slugs = db.StringListProperty()
  slug = db.StringProperty()
  isPublished = db.BooleanProperty()


class Product(db.Model):
  company = db.ReferenceProperty(Company)
  name = db.StringProperty()
  slugs = db.StringListProperty()
  slug = db.StringProperty()
  description = db.TextProperty()
  notes = db.TextProperty()
  picture = db.BlobProperty()
  auPrice = db.FloatProperty()
  auPriceIncludesGst = db.BooleanProperty()
  cheaperCountry = db.StringProperty()
  cheaperCurrency = db.StringProperty()
  cheaperPrice = db.FloatProperty()
  cheaperPriceIncludesTax = db.BooleanProperty()
  proof = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  updated = db.DateTimeProperty(auto_now=True)
  isPublished = db.BooleanProperty()


