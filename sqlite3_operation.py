'''
create 2013-4-9
@author h&m
'''
import sqlite3
import log_behavior
#/root/chinese_websites/websites_cn.db
class sqlite3_operation(object):
	def __init__(self, dbfile):
		self.dbfile = dbfile
		self.log = log_behavior.log()
	
	def _connect(self):
		try:
			self.conn = sqlite3.connect(self.dbfile)
			self.cur = self.conn.cursor()
			self.conn.isolation_level = None
		except Exception as err:
			print "error"
			log.log_error("connect db happens %s" %str(err))

	def execDB(self, execsql):
		print execsql
		result = self.conn.execute(execsql)
		self.conn.commit()
		return result
	
			
	def getResult(self, selectsql):
		self.cur.execute(selectsql)	
		self.res = self.cur.fetchall()
		self.log.log_info("select db")
		return self.res

	def getCount(self):
		return len(self.res)
	
	def closeDB(self):
		self.cur.close()
		self.conn.close()


#if __name__ == "__main__":
#	dbfile = "/root/chinese_websites/websites_cn.db"
#	insertsql = "insert into user(name) values('e')"
#	i = 1
#	selectsql = ("select * from user where id = %d" %i)
	
#	db_operation = sqlite3_operation(dbfile)
#	db_operation._connect()
#	db_operation.execDB(insertsql).fetchall()
#	res = db_operation.getResult(selectsql)
#	db_operation.getCount()
#	db_operation.closeDB()
			
#	for line in res:
#		for col in line:
#			print col
	
