# -*- coding:utf-8 -*-
#  ________________________________________
# / Talking much about oneself can also be \
# | a means to conceal oneself.            |
# |                                        |
# \ -- Friedrich Nietzsche                 /
#  ----------------------------------------
#         \   ^__^
#          \  (OO)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||

from main import logger
import requests
import json

class Webhook(object):
  def __init__(self):
    pass

  def send_msg(self):
    pass

class LarkHook(Webhook):
  def __init__(self, config):
    self.webhook = config.webhook
  def send_msg(self, msg):
    r = requests.request('POST',
                       self.webhook,
                       headers={
                         "Content-Type":"application/json"
                       }
                       ,data=json.dumps(msg))
    return r
