#!/usr/bin/python

# TODO - it would be nice if domains were somehow protected
# from one another... i think that's impossible, however
import anydbm, os

def key(user, domain):
    return '%s@%s' % ( user, domain )

def put(user, domain, val):
    db[key(user, domain)] = val

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
            val = form.getfirst('val')
            callback = form.getfirst('callback')

            result = {}
            result['success'] = False
            if user != None and domain != None:
                if val is None:
                    val = get(user, domain)
                    result['val'] = val
                    result['success'] = True
                else:
                    put(user, domain, val)
                    result['success'] = True
            print "Content-type: application/json\r\n\r\n",
            data = json.dumps(results)
            if callback != None:
                data = '%s(%s)' % ( callback, data )
            print data
        else:
            import sys
            if len(sys.argv) == 3:
                _, user, domain = sys.argv
                print get(user, domain)
            elif len(sys.argv) == 4:
                _, user, domain, val = sys.argv
                put(user, domain, val)
            else:
                print 'Usage: %s user domain val' % sys.argv[0]
                sys.exit(1)

finally:
    db.close()
