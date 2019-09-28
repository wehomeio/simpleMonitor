# -*- coding:utf-8 -*-
#  ______________________________________
# / If builders built buildings the way  \
# | programmers wrote programs, then the |
# | first woodpecker to come along would |
# \ destroy civilization.                /
#  --------------------------------------
#         \   ^__^
#          \  (OO)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||

class BaseConfig(object):
  """
  Base config for settings
  tmp_folder: tmp folder to store backup files
  tmp_
  """
  def __init__(self, config):
    self.dry_run = config.get("dry_run") or False
    # default to True
    self.delete_tmp_file = config.get("delete_tmp_file") if config.get("delete_tmp_file") is not None else True
    self.tmp_folder = config["tmp_folder"]
    self.passphrase = config["passphrase"]
    self.log_file = config["log_file"]


class LarkConfig(object):
  """
  Config for webhook
  """
  def __init__(self, config): 
    self.webhook = config["webhook"]

class SQLConfig(object):
  """
  Config for SQL monitoring
  """
  def __init__(self, config):
    self.host = config["host"]
    self.database = config["database"]
    self.tables = config["tables"]
    self.username = config["username"]
    # ToDo: put into databag
    self.password = config["password"]
    # monitor interval: Every n minutes
    self.interval = config["interval"]
    self.interval_unit = config["interval_unit"]


