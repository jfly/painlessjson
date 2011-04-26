#!/usr/bin/python

import cgi, cgitb, Cookie, os, datetime
try:
	import json
except ImportError:
	import simplejson as json

cgitb.enable()


form = cgi.FieldStorage()
value = form.getfirst('value')
callback = form.getfirst('callback')

cookie = Cookie.SimpleCookie()

if value != None:
	cookie['value'] = value
	expiration = datetime.datetime.now() + datetime.timedelta(days=30)
	expires = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
	print "%s; expires=%s;" % ( cookie, expires )
else:
	cookie.load(os.environ.get("HTTP_COOKIE", ""))

data = {}
if 'value' in cookie:
	data['value'] = cookie['value'].value
	data['foo'] = 'bar'

data = json.dumps(data)
if callback is None:
	contentType = 'application/json'
else:
	contentType = 'application/javascript'
	data = '%s(%s)' % ( callback, data )

print "Content-type: %s\r\n\r\n" % contentType,
print data
