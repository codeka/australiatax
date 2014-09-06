
import jinja2
import logging
import os
import re


jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/../tmpl'))


def _filter_dump_json(obj):
  return json.dumps(obj)
jinja.filters['dump_json'] = _filter_dump_json


def _filter_number(n):
  return "{:,}".format(n)
jinja.filters["number"] = _filter_number


def getTemplate(tmpl_name):
  return jinja.get_template(tmpl_name)


def render(tmpl, data):
  return tmpl.render(data)
