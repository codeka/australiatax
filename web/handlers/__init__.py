import datetime
import json
import logging
import os
import time
import urllib
import webapp2 as webapp

from google.appengine.api import memcache
from google.appengine.api import users

import ctrl.tmpl


# This value gets incremented every time we deploy so that we can cache bust
# our static resources (css, js, etc)
RESOURCE_VERSION = 3


class BaseHandler(webapp.RequestHandler):
  """Base class for all handlers, has some helper methods for rendering and so on."""
  def dispatch(self):
    """Dispatches the current request."""
    self.user = users.get_current_user()
    super(BaseHandler, self).dispatch()

  def render(self, tmplName, args):
    """Renders the given template. We add a bit of extra data to the args that is common for everybody."""
    user = users.get_current_user()

    if not args:
      args = {}

    args['year'] = datetime.datetime.now().year

    if os.environ['SERVER_SOFTWARE'].startswith('Development'):
      args['is_development_server'] = True
      args['resource_version'] = int(time.time())
    else:
      args['is_development_server'] = False
      args['resource_version'] = RESOURCE_VERSION

    if tmplName[-4:] == ".txt":
      self.response.content_type = "text/plain"
    elif tmplName[-4:] == ".rss":
      self.response.content_type = "application/rss+xml"
    else:
      self.response.content_type = "text/html"

    tmpl = ctrl.tmpl.getTemplate(tmplName)
    self.response.out.write(ctrl.tmpl.render(tmpl, args))

  def error(self, code):
    """Handles errors. We have a custom 404 error page."""
    super(BaseHandler, self).error(code)
    if code == 404:
      self.render("404.html", {})

  def _isLoggedIn(self, is_required=True):
    """For pages that require a logged-in user, this can be called to ensure you're logged in."""
    self.user = users.get_current_user()
    if not self.user and is_required:
      # not logged in, so redirect to the login page
      self.redirect(users.create_login_url(self.request.path_qs))
      return False

    return True

