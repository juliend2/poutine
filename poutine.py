
	#~POUTINE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
	#									  #
	# It's a Web nano-framework in Python #
	#									   #
	#~Enjoy!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import inspect
import sys
import os
import wsgiref.util as wsgi
from urlparse import urlparse, urlunparse, urlsplit


class Poutine:
	# poutine-related :
	environ = {}
	retval = {}
	def __init__(self, environ):
		self.environ = environ
		self.retval = { #or : 303 See Other , or 404 Not Found
			'output':'', \
			'status':'200 OK', \
			'location':'' \
		}
		self.qs = self.getquerystring()
		
	def dispatch(self):
		self.retval['output'] = getattr(self, self.qs['action'])() # override
		return self.retval # Return the response Dictionary

	def getpath(self):
		return "\n".join(sys.path)

	def respond404(self):
		self.retval['status'] = '404 Not Found'
		self.retval['output'] = ''
		return self.retval

	def redirect(self, address):
		self.retval['output'] = ''
		self.retval['status'] = '303 See Other'
		self.retval['location'] = '?action='+address
		return self.retval

	def getquerystring(self):
		qs = self.environ['QUERY_STRING']
		return self.parse_qs(qs)

	def getkey(self, key):
		qs = self.environ['QUERY_STRING']
		return self.parse_qs(qs)[key]
		
	def getpost(self):
		try:
			request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0
		request_body = self.environ['wsgi.input'].read(request_body_size)
		# print >> self.environ['wsgi.errors'], str(self.parse_qs(request_body)) # debugging technique , more info at : http://code.google.com/p/modwsgi/wiki/DebuggingTechniques
		return self.parse_qs(request_body)

	def parse_qs(self, qs):
		"""
		parse query string
		"""
		if qs == '':
			return {}
		else:
			querylist = qs.split('&')
			if len(querylist) < 1 :
				return {}
			else:
				querydict = {}
				for item in querylist:
					lis = item.split('=')
					querydict[lis[0]] = lis[1]
				return querydict


