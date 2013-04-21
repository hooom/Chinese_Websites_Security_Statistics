import socket
from OpenSSL import SSL, crypto
import log_behavior
import time

class cert_fetch(object):
	def __init__(self):
		self.context = SSL.Context(SSL.SSLv23_METHOD)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(30)
		self.connection = SSL.Connection(self.context, self.sock)
		self.log = log_behavior.log()
		self.cert_path = "certificates_cn/"
		self.cert_chain_path = "certificates_chain_cn/"


	def _get_context(self):
		return self.context

	def _connect(self, domainname):
		self.connection.connect((domainname, 443))
		self.connection.setblocking(1)
		(ip, port) = self.connection.getpeername()
		self.domainname = domainname
		self.ip = ip
		print "ip:" + self.ip
		try:
    			self.connection.do_handshake()
			self.log.log_info(time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+"connected to "+ domainname + ":443 "+self.connection.state_string())
		except SSL.WantReadError as err:
			self.log.log_error(time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+str(err))

	def _get_ip(self):
		return self.ip

	def _get_domainname(self):
		return self.domainname
			
	 
	def _get_cert(self):
		#return X509 Object
		self.cert = self.connection.get_peer_certificate()
		return self.cert

	def _get_cert_subject_cn(self):
		subject_common_name = self.cert.get_subject().commonName
		if(subject_common_name is None):
			return ''
		else:
			return subject_common_name

	def _get_cert_issuer_cn(self):
		issuer_common_name =  self.cert.get_issuer().commonName
		if(issuer_common_name is None):
			return ''
		else:
			return issuer_common_name

	def _get_cert_name(self):
		return self.cert_path + self.domainname + "+" + self.ip + ".pem"

	def _save_cert(self):
		try:
			#crypto.dump_certificate(crypto.FILETYPE_PEM,X509)
			self.cert_file = open(self.cert_path + self.domainname + "+" + self.ip + ".pem", "w")
			self.cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM,self.cert))
			self.log.log_info(time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+"save certificate about " + self.domainname + " & " + self.ip)
		except IOError as err:
			self.log.log_error(time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+"save " + self.domainname + " & " + self.ip + " cert fail")
		self.cert_file.close()
	
	def _get_cert_chain(self):
		#return list X509 Object
		self.cert_chain = self.connection.get_peer_cert_chain()
		return self.cert_chain

	def _get_cert_chain_name(self):
		return self.cert_chain_path + self.domainname + "+" + self.ip + "+chain.pem"

	def _get_cert_chain_depth(self):
		return len(self.cert_chain)

	def _save_cert_chain(self):
		try:
			self.cert_chain_file = open(self.cert_chain_path + self.domainname + "+" + self.ip + "+chain.pem", "a")
			for item in self.cert_chain:
				self.cert_chain_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM,item))
		except IOError as err:
			self.log.log_error(time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+"save cert chain" + self.domainname + " & " + self.ip + " cert fail")
		self.cert_chain_file.close()

	def _verify_chain(self):
		pass

	def _has_expired(self):
		return self.cert.has_expired()
	
	def _get_verify_depth(self):
		pass
	
	def _close(self):
		self.connection.close()

#fetch = cert_fetch()	
#fetch._connect("www.alipay.com")
#print fetch._get_context().get_verify_depth()
#fetch._get_cert()
#print "has_expired:" + str(fetch._has_expired())
#fetch._save_cert()
#fetch._get_cert_chain()
#fetch._save_cert_chain()	
#print fetch._get_cert_subject_cn()
#print fetch._get_cert_chain_depth()

