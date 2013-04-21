import logging

#logger = logging.getLogger()
#handler =  logging.FileHandler("db&op.log")
#logger.addHandler(handler)
#logger.setLevel(logging.NOTSET)
class log(object):
	def __init__(self, logfile = "db&op.log"):
		self.logger = logging.getLogger()
		self.logfile = logfile
		self.handler =  logging.FileHandler(self.logfile)
		self.logger.addHandler(self.handler)
		self.logger.setLevel(logging.NOTSET)

	def log_error(self, str):
		self.logger.error(str)

	def log_info(self, str):
		self.logger.info(str)

	def log_warning(str):
		self.logger.warning(str)

	def log_critical(self, str):
		self.logger.critical(str)

	def log_debug(self, str):
		self.logger.debug(str)
	
