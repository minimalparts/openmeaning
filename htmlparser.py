import re
import sys
import logging
import requests
from models import Url
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def extract_from_url(url):
    '''From history info, extract url, title and body of page,
    cleaned with BeautifulSoup'''
    req = requests.get(url, allow_redirects=True, timeout=10)
    req.encoding = 'utf-8'
    if req.status_code is not 200:
      logging.exception("Warning: "  + str(req.url) + ' has a status code of: ' \
        + str(req.status_code) + ' omitted from database.\n')
    bs_obj = BeautifulSoup(req.text,"lxml")
    if hasattr(bs_obj.title, 'string') & (req.status_code == requests.codes.ok):
        if url.startswith('http'):
          title = bs_obj.title.string
          checks = ['script', 'style', 'meta', '<!--']
          for chk in bs_obj.find_all(checks):
            chk.extract()
          body = bs_obj.get_text()
          pattern = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
          body_str=re.sub(pattern," ",body)
          snippet = body_str[:100].replace(',','-')
          if title is None:
            title = u'Untitled'
          u = Url(url=url, title=title, snippet = snippet)
    logging.exception ("Processed",url,"...")
    logging.exception(u.title,body_str)
    return u,body_str
    # can't connect to the host

