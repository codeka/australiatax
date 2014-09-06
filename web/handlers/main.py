
import os
import datetime
import webapp2 as webapp

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users
from datetime import datetime, timedelta
import json

import ctrl
import ctrl.products
import handlers
import model.products

class BasePage(handlers.BaseHandler):
  pass


class HomePage(BasePage):
  def get(self):
    self.render('index.html', {})


class ProductsPage(BasePage):
  def get(self):
    products = ctrl.products.getProductList(0, 25)
    self.render('products/list.html', {'products': products})


class NewProductPage(BasePage):
  def get(self):
    self.render('products/new.html', {})

  def post(self):
    companyName = self.request.POST.get('company')
    companySlug = ctrl.makeSlug(companyName)
    companyMdl = model.products.Company.all().filter('slugs =', companySlug).fetch(1)
    if not companyMdl:
      companyMdl = model.products.Company(name=companyName, slugs=[companySlug], slug=companySlug, isPublished=False)
      companyMdl.put()
    else:
      companyMdl = companyMdl[0]

    productName = self.request.POST.get('name')
    productSlug = ctrl.makeSlug(productName)
    productMdl = model.products.Product.all().filter('slugs =', productSlug).fetch(1)
    if not productMdl:
      pictureBlob = images.resize(self.request.get('picture'), 900)
      productMdl = model.products.Product(name=productName, slugs=[productSlug], slug=productSlug, isPublished=False,
                                          company=companyMdl,
                                          description=self.request.POST.get('description'),
                                          notes=self.request.POST.get('notes'),
                                          picture=db.Blob(pictureBlob),
                                          auPrice=float(self.request.POST.get('au-price')),
                                          auPriceIncludesGst=self.request.POST.get('includes-gst') == 1,
                                          cheaperCountry=self.request.POST.get('country-available'),
                                          cheaperCurrency=self.request.POST.get('overseas-price'),
                                          cheaperPrice=float(self.request.POST.get('overseas-price')),
                                          cheaperPriceIncludesTax=self.request.POST.get('overseas-tax') == 1,
                                          proof=self.request.POST.get('proof'))
      productMdl.put()
      self.redirect("/products")
    else:
      # TODO: update product
      pass


class ProductDetailPage(BasePage):
  def get(self, companySlug, productSlug):
    productMdl = ctrl.products.getProductBySlugs(companySlug, productSlug)
    if not productMdl:
      self.error(404)

    self.render('products/details.html', {'product': productMdl})


class ProductImagePage(BasePage):
  def get(self, companySlug, productSlug):
    productMdl = ctrl.products.getProductBySlugs(companySlug, productSlug)
    if not productMdl:
      self.error(404)

    width = 900
    if self.request.get('width'):
      width = int(self.request.get('width'))
    height = 400
    if self.request.get('height'):
      height = int(self.request.get('height'))

    img = images.Image(productMdl.picture)
    if img.width > width or img.height > height:
      img.resize(width=width, height=height)
    img.im_feeling_lucky()
    img = img.execute_transforms(output_encoding=images.JPEG)

    self.response.headers['Content-Type'] = 'image/jpeg'
    self.response.out.write(img)


app = webapp.WSGIApplication([('/?', HomePage),
                              ('/products', ProductsPage),
                              ('/products/new', NewProductPage),
                              ('/products/([^/]+)/([^/]+)', ProductDetailPage),
                              ('/products/([^/]+)/([^/]+)/img', ProductImagePage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
