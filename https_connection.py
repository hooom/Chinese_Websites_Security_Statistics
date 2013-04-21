'''
create 2013-4-8
@author h&m
'''
import requests

class https_connection:

	def connection(self, strs):
		try:
			self.rawurl = strs
			r = requests.get(strs,verify=False)
			return r
		except Exception as err:
			return str(type(err[0])).split("'")[1]		

	
	def https_is_redirect(self, r):	
		if(isinstance(r,requests.models.Response)):
			if(len(r.history) > 0):
				if r.history[0].status_code in [301,302,303,307]:
					return 1
			else:
				return 0
		else:
			return 0
	
	def https_is_open(self, r):
		if(isinstance(r,requests.models.Response)):
			if(len(r.history) ==  0):
				if r.status_code is not None:
					return 1
				else:
					return 0
			else:
				if(self.https_ultimate_protocol(r) == 'https'):
					return 1
				else:
					return 0
		else:
			return 0

	def https_error(self, r):
		if(isinstance(r,requests.models.Response)):
			if(len(r.history) ==  0 and r.status_code is not None):
				if r.status_code != 200:
					return str(r.status_code)
		if(not isinstance(r,requests.models.Response)):
			return r
		else:
			return '';

	def https_redirect_number(self, r):
		if(isinstance(r,requests.models.Response)):
                	return len(r.history)
		return 0

#problem
	def https_ultimate_url(self, r):
		if(isinstance(r,requests.models.Response)):
			if(self.https_is_redirect(r) == 1):
				location = r.history[-1].headers.get('location')
                                if(location[0:4] == 'http' or location[0:4] == 'www.'):
                                        return location
                                else:
                                        return self.rawurl + location
			else:
				return r.url
		else:
			return ''

	def https_ultimate_domainname(self, r):
		url = self.https_ultimate_url(r)
		if(len(url) > 0):
			if(url[0:8] == 'https://' or url[0:7] == 'http://'):
                                return url.split('/')[2]
                        else:
                                return url.split('/')[0]
		else:
			return ''

	def https_ultimate_protocol(self, r):
		url = self.https_ultimate_url(r)
		if(len(url) > 0):
			if(url[0:5] == 'https'):
				return 'https'
			if(url[0:4] == 'http'):
				return 'http'
		else:
			return ''
			
conn = https_connection()
r = conn.connection("https://www.abchina.com")
print conn.https_ultimate_url(r)
#print conn.https_ultimate_url(r)
#print(conn.https_is_redirect(r))
#print(conn.https_ultimate_domainname(r))
