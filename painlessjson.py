#!/usr/bin/python

# TODO - it would be nice if domains were somehow protected
# from one another... i think that's impossible, however
import anydbm

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
        import sys
        if len(sys.argv) == 3:
            _, user, domain = sys.argv
            print(get(user, domain))
        elif len(sys.argv) == 4:
            _, user, domain, val = sys.argv
            put(user, domain, val)
        else:
            print('Usage: %s user domain val' % sys.argv[0])
            sys.exit(1)
    else:
        import cgi, cgitb, json
        cgitb.enable()

        # TODO - error checking
        form = cgi.FieldStorage()
        user = form.getfirst('user')
        domain = form.getfirst('domain')
        val = form.getfirst('val')
        callback = form.getfirst('callback')

        result = {}
        if val is None:
            val = get(user, domain)
            result['val'] = val
        else:
            put(user, domain, val)
        result['success'] = True
        print("Content-type: application/json")
        print()
        print(json.dumps(result))

finally:
    db.close()
