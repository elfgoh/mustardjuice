try: config=open('routes.conf','r').read()
except: config=''

def auto_in(apps):
    routes=[
        ('/robots.txt','/welcome/static/robots.txt'),
        ('/favicon.ico','/welcome/static/favicon.ico'),
        ('/admin$anything','/admin$anything'),
        ]
    for a,b in [x.strip().split() for x in apps.split('\n') if x.strip() and not x.strip().startswith('#')]:
        if not b.startswith('/'): b='/'+b
        if b.endswith('/'): b=b[:-1]
        app = b.split('/')[1]
        routes+=[
            ('.*:https?://(.*\.)?%s:$method /' % a,'%s' % b),
            ('.*:https?://(.*\.)?%s:$method /static/$anything' % a,'%s/static/$anything' % app),
            ('.*:https?://(.*\.)?%s:$method /appadmin/$anything' % a,'%s/appadmin/$anything' % app),
            ('.*:https?://(.*\.)?%s:$method /$anything' % a,'%s/$anything' % b), 
            ]
    return routes

def auto_out(apps):
    routes=[]
    for a,b in [x.strip().split() for x in apps.split('\n') if x.strip() and not x.strip().startswith('#')]:
        if not b.startswith('/'): b='/'+b
        if b.endswith('/'): b=b[:-1]
        app = b.split('/')[1]
        routes+=[
            ('%s/static/$anything' % app,'/static/$anything'),
            ('%s/appadmin/$anything' % app, '/appadmin/$anything'),
            ('%s/$anything' % b, '/$anything'),
            ]
    return routes

routes_in=auto_in(config)
routes_out=auto_out(config)
