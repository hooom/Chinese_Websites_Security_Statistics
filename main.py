import log_behavior
import sqlite3_operation
import time
import http_connection
import https_connection
import certificates_fetch
import socket
import datetime
from gevent.coros import Semaphore
from gevent.greenlet import Greenlet
from gevent import sleep
import random
semaphore = Semaphore()
starttime = datetime.datetime.now()
f_cn_sites = open("../test_banks.csv", "r")

#open db
#connect db
dbfile = "/root/chinese_websites/websites_cn.db"
db = sqlite3_operation.sqlite3_operation(dbfile)
db._connect()

	#read source domainname 
	#../china_banks.csv
#	f_cn_sites = open("../china_banks.csv", "r")

	#open db
	#connect db
 #       dbfile = "/root/chinese_websites/websites_cn.db"
  #      db = sqlite3_operation.sqlite3_operation(dbfile)
   #     db._connect()
def task():
	while True:
		semaphore.acquire()
		line = f_cn_sites.readline().strip()
		if(line == ''):
			break
		print line
		website_property = "business"
		domain_name = line
		#http is open, no->http_error yes-->directory
		#initial http connection
		http_conn = http_connection.http_connection()
		req_http = http_conn.connection("http://" + line)
	
		http_is_open = http_conn.http_is_open(req_http)
		http_is_redirect = http_conn.http_is_redirect(req_http)
		http_error = http_conn.http_error(req_http)
		http_error = http_conn.http_error(req_http)
		http_redirect_number = http_conn.http_redirect_number(req_http)
		http_ultimate_url = http_conn.http_ultimate_url(req_http)
		http_ultimate_domainname = http_conn.http_ultimate_domainname(req_http)
		http_ultimate_protocol = http_conn.http_ultimate_protocol(req_http)

	
		
		#https is open? no -> crawler source page, yes ---> directory & fetch cert
		https_conn = https_connection.https_connection()
        	req_https = https_conn.connection("https://" + line)
        
        	https_is_open = https_conn.https_is_open(req_https)
        	https_is_redirect = https_conn.https_is_redirect(req_https)
		https_error = https_conn.https_error(req_https)
        	https_redirect_number = https_conn.https_redirect_number(req_https)
        	https_ultimate_url = https_conn.https_ultimate_url(req_https)
        	https_ultimate_domainname = https_conn.https_ultimate_domainname(req_https)
        	https_ultimate_protocol = https_conn.https_ultimate_protocol(req_https) 
		
		global cert_name, cert_chain_name, ip, has_expired, subject_cn, issuer_cn, cert_chain_depth
		#get certifcates
		if(https_is_open == 1):
			#initial class
			fetch = certificates_fetch.cert_fetch()
			fetch._connect(line)
			#cert
			fetch._get_cert()
			fetch._save_cert()
			cert_name = fetch._get_cert_name()
			#cert chain
			fetch._get_cert_chain()
			fetch._save_cert_chain()
			cert_chain_name = fetch._get_cert_chain_name()
			
			ip = fetch._get_ip()
			has_expired = fetch._has_expired()
			
			subject_cn = fetch._get_cert_subject_cn()
			issuer_cn = fetch._get_cert_issuer_cn()
			
		 	cert_chain_depth = fetch._get_cert_chain_depth()
			fetch._close()

		else:
			cert_name = ''
			cert_chain_name = ''
			try:
				ip = socket.getaddrinfo(line, 'http')[0][4][0]
			except Exception as err:
				ip = str(type(err[0])).split("'")[1] 
			has_expired = -1
			subject_cn = ''
			issuer_cn = ''
			cert_chain_depth = -1
			
	
		#test
		print '##################'
		print domain_name
		print ip
		print website_property
		print http_is_open
		print http_error
		print https_is_open
		print https_error
		print cert_name
		print has_expired
		print cert_chain_name
		print subject_cn
		print issuer_cn
		print cert_chain_depth
		print http_is_redirect
		print http_redirect_number
		print http_ultimate_url
		print http_ultimate_domainname
		print http_ultimate_protocol
		print https_is_redirect
		print https_redirect_number
		print https_ultimate_url
		print https_redirect_number
		print https_ultimate_url
		print https_ultimate_domainname
		print https_ultimate_protocol

		print '#######################'	
		#insert new record
		insertsql = "insert into websites_cn_statistic(domain_name,ip,website_property,http_is_open, \
				http_error,https_is_open,https_error,cert_name,has_expired, \
				cert_chain_name,subject_cn,issuer_cn,cert_chain_depth, \
				http_is_redirect,http_redirect_number,http_ultimate_url, \
				http_ultimate_domainname,http_ultimate_protocol,https_is_redirect, \
				https_redirect_number,https_ultimate_url,https_ultimate_domainname, \
				https_ultimate_protocol) values('"+ domain_name + "','" + ip+ "','" +\
				website_property+ "'," +str(http_is_open)+ ",'" +\
                                http_error+ "'," +str(https_is_open)+ ",'" +https_error\
				+ "','" +\
				cert_name+ "'," +str(has_expired)+ ",'" +cert_chain_name+ "','" +\
				subject_cn+ "','" +issuer_cn+ "'," +str(cert_chain_depth)+ "," +\
                                str(http_is_redirect)+ "," +str(http_redirect_number)+ ",'" +\
				http_ultimate_url+ "','" +\
                                http_ultimate_domainname+ "','" +http_ultimate_protocol+ "'," +\
				str(https_is_redirect)+ "," +str(https_redirect_number)+ ",'" +\
				https_ultimate_url+ "','" +https_ultimate_domainname+"','"+\
				https_ultimate_protocol+"')"
		print insertsql
		db.execDB(insertsql)
		semaphore.release()
gs = []
for i in xrange(10):
	gs.append(Greenlet.spawn(task))
for g in gs:
	g.join()

db.closeDB()
endtime = datetime.datetime.now()
interval = (endtime - starttime).seconds
print interval
