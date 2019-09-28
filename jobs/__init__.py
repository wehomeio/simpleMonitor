# -*- coding:utf-8 -*-

#  ________________________________________
# / The way to love anything is to realize \
# \ that it might be lost.                 /
#  ----------------------------------------
#         \   ^__^
#          \  (OO)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||

import delegator
import datetime
import os
import re

from helper import with_logging
from main import logger

LINE_LENGTH = 80
MSG_LENGTH = 600
SPLIT_KEYWORD = 'INSERT'

class MonitorJob(object):
  """
  base class for backup jobs
  real jobs should extend this class
  """
  def __init__(self):
    pass

  def run(self):
    pass

  @staticmethod
  def safe_delete(file_path):
    if os.path.isfile(file_path):
      os.remove(file_path)
      logger.info("deleted file {}".format(file_path))

  @staticmethod
  def construct_filename_with_path(base_folder, database, table, suffix, ext='sql'):
    '''
    folder/db-table-previous/current.sql
    '''
    tmp_file_name = "{}-{}-{}.{}".format(
        database, 
        table,
        suffix,
        ext
      )

    tmp_file_name_with_path = "{}/{}".format(base_folder, tmp_file_name)

    return tmp_file_name_with_path

class Heartbeat(MonitorJob):
  """
  Heartbeat
  """
  def __init__(self, n):
    self.counter = 0
    self.internal = n

  def run(self):
    self.counter += 1
    logger.info("Heartbeat for every {} seconds. Total time is {}".format(self.internal, self.counter))

class SqlMonitorJob(MonitorJob):
  """
  Back up a mysql database
  """

  def __init__(self, base_config, sql_config, webhook):
    self.base_config = base_config
    self.sql_config = sql_config
    self.webhook = webhook

  def reconstruct_msg(self, diff_msg):
    msgs = re.findall('INSERT.+',diff_msg)
    combined = "\n".join(map(lambda x: x[0:100], msgs))
    return(combined[0:MSG_LENGTH])

  @with_logging
  def run(self):
    base_folder = self.base_config.tmp_folder
    database = self.sql_config.database
    for table in self.sql_config.tables:
      previous_dump_name = MonitorJob.construct_filename_with_path(base_folder, database, table, "previous")
      current_dump_name = MonitorJob.construct_filename_with_path(base_folder, database, table, "current")

      try:
        # dump sql to file
        # mysqldump --skip-comments --skip-extended-insert -u root -p db table > file.sql
        sql_dump_command = "mysqldump --skip-comments --skip-extended-insert -h{} -u{} -p{} {} {} > {}".format(
            self.sql_config.host, 
            self.sql_config.username,
            self.sql_config.password,
            database,
            table,
            current_dump_name
          ) if self.sql_config.password else "mysqldump --skip-comments --skip-extended-insert -h{} -u{} {} {} > {}".format(
            self.sql_config.host, 
            self.sql_config.username,
            database,
            table,
            current_dump_name
          )

        command = sql_dump_command
        logger.debug("running {}".format(command))
        c = delegator.run(command)
        if c.return_code != 0:
          raise RuntimeError(c.std_err)

        # Compare and send
        command = "diff {} {}".format(previous_dump_name, current_dump_name)
        logger.debug("running {}".format(command))
        c = delegator.run(command)

        if c.return_code == 1:
          msg = {
            "title": "Diff on {}-{}".format(database, table),
            "text": self.reconstruct_msg(c.out)
          }
          logger.debug(msg)

          self.webhook.send_msg(msg)
        else:
          logger.error("Diff failed {}".format(c.err))

        # move file
        os.rename(current_dump_name, previous_dump_name)
        MonitorJob.safe_delete(current_dump_name)

      except (RuntimeError, AssertionError) as  e:
        # log
        logger.error(e)
