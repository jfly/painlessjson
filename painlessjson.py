#!/usr/bin/python

# TODO - it would be nice if domains were somehow protected
# from one another... i think that's impossible, however
import anydbm, os

def key(user, domain):
    return '%s@%s' % ( user, domain )

def put(user, domain, value):
    db[key(user, domain)] = value

def get(user, domain):
    k = key(user, domain)
    return db.get(k, '')

try:
    db = anydbm.open('json', 'c')
    if __name__ == "__main__":
        if 'QUERY_STRING' in os.environ:
            import cgi, cgitb
            try:
                import json
            except ImportError:
                import simplejson as json
            cgitb.enable()

            # TODO - error checking
            form = cgi.FieldStorage()
            user = form.getfirst('user')
            domain = form.getfirst('domain')
            value = form.getfirst('value')
            callback = form.getfirst('callback')

            result = {}
            result['success'] = False
            if user != None and domain != None:
                if value is None:
                    value = get(user, domain)
                    result['value'] = value
                    result['success'] = True
                else:
                    put(user, domain, value)
                    result['value'] = value
                    result['success'] = True

            contentType = 'application/json'
            data = json.dumps(result)
            if callback != None:
                contentType = 'application/javascript'
                data = '%s(%s)' % ( callback, data )
            print "Content-type: %s\r\n\r\n" % contentType,
            print data
        else:
            import sys
            if len(sys.argv) == 3:
                _, user, domain = sys.argv
                print get(user, domain)
            elif len(sys.argv) == 4:
                _, user, domain, value = sys.argv
                put(user, domain, value)
            else:
                print 'Usage: %s user domain value' % sys.argv[0]
                sys.exit(1)

finally:
    db.close()
