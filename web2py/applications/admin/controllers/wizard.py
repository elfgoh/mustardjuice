# -*- coding: utf-8 -*- 

import os, uuid, re, pickle, urllib, glob
from gluon.admin import app_create, plugin_install
from gluon.fileutils import abspath

def reset(session):
    session.app={
        'name':'',
        'params':[('title','My New App'),
                  ('subtitle','powered by web2py'),
                  ('author','you'),
                  ('author_email','you@example.com'),
                  ('keywords',''),
                  ('description',''),
                  ('layout_theme','Default'),
                  ('database_uri','sqlite://storage.sqlite'),
                  ('security_key',str(uuid.uuid4())),
                  ('email_server','localhost'),
                  ('email_sender','you@example.com'),
                  ('email_login',''),                  
                  ('login_method','local'),
                  ('login_config','')],
        'tables':['auth_user'],
        'table_auth_user':['username','first_name','last_name','email','password'],
        'pages':['index','error'],
        'page_index':'# Welcome to my new app',
        'page_error':'# Error: the document does not exist',
        }

if not session.app: reset(session)

def listify(x):
    if not isinstance(x,(list,tuple)):
        return x and [x] or []
    return x

def clean(name):
    return re.sub('\W+','_',name.strip().lower())

def index():
    response.view='wizard/step.html'
    reset(session)
    apps=os.listdir(os.path.join(request.folder,'..'))
    form=SQLFORM.factory(Field('name',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC()]))
    if form.accepts(request.vars):
        app = form.vars.name
        session.app['name'] = app
        if app in apps:
            meta = os.path.join(request.folder,'..',app,'wizard.metadata')
            if os.path.exists(meta):
                try:
                    session.app=pickle.load(open(meta,'rb'))
                    session.flash = "The app exists, was created by wizard, continue to overwrite!"
                except:
                    session.flash = "The app exists, was NOT created by wizard, continue to overwrite!"
        redirect(URL('step1'))
    return dict(step='Start',form=form)
                         

def step1():
    from gluon.contrib.simplejson import loads
    import urllib
    if not session.themes:
        url=LAYOUTS_APP+'/default/layouts.json'
        try:
            data = urllib.urlopen(url).read()
            session.themes = ['Default']+loads(data)['layouts']
        except:
            session.themes = ['Default']
    themes = session.themes
    response.view='wizard/step.html'
    params = dict(session.app['params'])
    form=SQLFORM.factory(
                Field('title',default=params.get('title',None),
                                      requires=IS_NOT_EMPTY()),
                Field('subtitle',default=params.get('subtitle',None)),
                Field('author',default=params.get('author',None)),
                Field('author_email',default=params.get('author_email',None)),
                Field('keywords',default=params.get('keywords',None)),
                Field('description','text',
                      default=params.get('description',None)),
                Field('layout_theme',requires=IS_IN_SET(themes),
                      default=params.get('layout_theme',themes[0])),
                Field('database_uri',default=params.get('database_uri',None)),
                Field('security_key',default=params.get('security_key',None)),
                Field('email_server',default=params.get('email_server',None)),
                Field('email_sender',default=params.get('email_sender',None)),
                Field('email_login',default=params.get('email_login',None)),
                Field('login_method',requires=IS_IN_SET(('local','janrain')),
                      default=params.get('login_method','local')),
                Field('login_config',default=params.get('login_config',None)))
                
    if form.accepts(request.vars):
        session.app['params']=[(key,form.vars.get(key,None)) 
                               for key,value in session.app['params']]
        redirect(URL('step2'))
    return dict(step='1: Setting Parameters',form=form)
        
def step2():  
    response.view='wizard/step.html'
    form=SQLFORM.factory(Field('table_names','list:string',
                               default=session.app['tables']))
    if form.accepts(request.vars):
        session.app['tables']=[clean(t)
                               for t in listify(form.vars.table_names)
                               if t.strip()]
        for table in session.app['tables']:
            if not 'table_'+table in session.app:
                session.app['table_'+table]=['name']
            if not table=='auth_user':
                for key in ['create','read','update','select','search']:
                    name = table+'_'+key
                    if not name in session.app['pages']:
                        session.app['pages'].append(name)
                        session.app['page_'+name]='## %s %s' % (key.capitalize(),table)
        if session.app['tables']:
            redirect(URL('step3',args=0))
        else:
            redirect(URL('step4'))
    return dict(step='2: Tables',form=form)

def step3():
    response.view='wizard/step.html'
    n=int(request.args(0) or 0)
    m=len(session.app['tables'])
    if n>=m: redirect(URL('step2'))
    table=session.app['tables'][n]
    form=SQLFORM.factory(Field('field_names','list:string',
                               default=session.app.get('table_'+table,[])))
    if form.accepts(request.vars) and form.vars.field_names:        
        fields=listify(form.vars.field_names)
        if table=='auth_user':
            for field in ['first_name','last_name','username','email','password']:
                if not field in fields:
                    fields.append(field)
        session.app['table_'+table]=[t.strip().lower()
                                       for t in listify(form.vars.field_names)
                                       if t.strip()]
        try:
            tables=sort_tables(session.app['tables'])
        except RuntimeError:
            response.flash=T('invalid circual reference')
        else:
            if n<m-1:
                redirect(URL('step3',args=n+1))
            else:
                redirect(URL('step4'))
    return dict(step='3: Fields for table "%s" (%s of %s)' % (table,n+1,m),table=table,form=form)

def step4():
    response.view='wizard/step.html'
    form=SQLFORM.factory(Field('pages','list:string',
                               default=session.app['pages']))
    if form.accepts(request.vars):
        session.app['pages']=[clean(t)
                              for t in listify(form.vars.pages)
                              if t.strip()]        
        if session.app['pages']:
            redirect(URL('step5',args=0))
        else:
            redirect(URL('step6'))
    return dict(step='4: Pages',form=form)

def step5():
    response.view='wizard/step.html'
    n=int(request.args(0) or 0)
    m=len(session.app['pages'])
    if n>=m: redirect(URL('step4'))
    page=session.app['pages'][n]
    markmin_url='http://web2py.com/examples/static/markmin.html'
    form=SQLFORM.factory(Field('content','text',
                               default=session.app.get('page_'+page,[]),
                               comment=A('use markmin',_href=markmin_url,_target='_blank')),
                         formstyle='table2cols')
    if form.accepts(request.vars):
        session.app['page_'+page]=form.vars.content
        if n<m-1:
            redirect(URL('step5',args=n+1))
        else:
            redirect(URL('step6'))
    return dict(step='5: View for page "%s" (%s of %s)' % (page,n+1,m),form=form)

def step6():
    response.view='wizard/step.html'
    params = dict(session.app['params'])
    app = session.app['name']
    form=SQLFORM.factory(
        Field('generate_model','boolean',default=True),
        Field('generate_controller','boolean',default=True),
        Field('generate_views','boolean',default=True),
        Field('generate_menu','boolean',default=True),
        Field('apply_layout','boolean',default=True),
        Field('erase_database','boolean',default=True),
        Field('populate_database','boolean',default=True))
    if form.accepts(request.vars):
        if DEMO_MODE:
            session.flash = T('Application cannot be generated in demo mode')
            redirect(URL('index'))
        create(form.vars)       
        session.flash = 'Application %s created' % app
        redirect(URL('generated'))
    return dict(step='6: Generate app "%s"' % app,form=form)

def generated():
    return dict(app=session.app['name'])

def sort_tables(tables):
    import re
    regex = re.compile('(%s)' % '|'.join(tables))
    is_auth_user = 'auth_user' in tables
    d={}
    for table in tables:
        d[table]=[]
        for field in session.app['table_%s' % table]:
            d[table]+=regex.findall(field)
    tables=[]
    if is_auth_user:
        tables.append('auth_user')
    def append(table,trail=[]):
        if table in trail: 
            raise RuntimeError
        for t in d[table]: append(t,trail=trail+[table])
        if not table in tables: tables.append(table)
    for table in d: append(table)
    return tables

def make_table(table,fields):
    rawtable=table
    if table!='auth_user': table='t_'+table
    s=''
    s+='\n'+'#'*40+'\n'
    s+="db.define_table('%s',\n" % table
    s+="    Field('id','id',\n"
    s+="          represent=lambda id:SPAN(id,' ',A('view',_href=URL('%s_read',args=id)))),\n"%rawtable
    first_field='id'
    for field in fields:
        items=[x.lower() for x in field.split()]
        has={}
        keys=[]
        for key in ['notnull','unique','integer','double','boolean','float',
                    'boolean', 'date','time','datetime','text','wiki',
                    'html','file','upload','image','true',
                    'hidden','readonly','writeonly','multiple',
                    'notempty','required']:
            if key in items[1:]:
                keys.append(key)
                has[key] = True
        tables = session.app['tables']
        refs = [t for t in tables if t in items]
        items = items[:1] + [x for x in items[1:] if not x in keys and not x in tables]
        barename = name = '_'.join(items)
        if table[:2]=='t_': name='f_'+name
        if first_field=='id': first_field=name

        ### determine field type
        ftype='string'
        for key in ['integer','double','boolean','float','boolean',
                    'date','time','datetime','text','file']:
            if key in has:
                ftype=key
        if 'wiki' in has or 'html' in has:
            ftype='text'
        elif 'file' in has or 'upload' in has or 'image' in has:
            ftype='upload'
        if refs:
            key = refs[0]
            if not key=='auth_user': key='t_'+key
            if 'multiple' in has:
                ftype='list:reference %s' % key
            else:
                ftype='reference %s' % key
        if ftype=='string' and 'multiple' in has:
            ftype='list:string'
        elif ftype=='integer' and 'multiple' in has:
            ftype='list:integer'
        elif name=='password':
            ftype='password'
        s+="    Field('%s', type='%s'" % (name, ftype)

        ### determine field attributes
        if 'notnull' in has or 'notempty' in has or 'required' in has:
            s+=', notnull=True'
        if 'unique' in has:
            s+=', unique=True'        
        if ftype=='boolean' and 'true' in has:
            s+=",\n          default=True"

        ### determine field representation
        if 'image' in has:
            s+=",\n          represent=lambda x: x and IMG(_alt='image',_src=URL('download',args=x), _width='200px') or ''"
        elif ftype in ('file','upload'):
            s+=",\n          represent=lambda x: x and A('download',_href=URL('download',args=x)) or ''"
        elif 'wiki' in has:
            s+=",\n          represent=lambda x: MARKMIN(x)"
            s+=",\n          comment='WIKI (markmin)'"
        elif 'html' in has:
            s+=",\n          represent=lambda x: XML(x,sanitize=True)"
            s+=",\n          comment='HTML (sanitized)'"
        ### determine field access
        if name=='password' or 'writeonly' in has:
            s+=",\n          readable=False"
        elif 'hidden' in has:
            s+=",\n          writable=False, readable=False"
        elif 'readonly' in has:
            s+=",\n          writable=False"

        ### make up a label
        s+=",\n          label=T('%s')),\n" % \
            ' '.join(x.capitalize() for x in barename.split('_'))
    if table!='auth_user':
        s+="    Field('active','boolean',default=True,\n"
        s+="          label=T('Active'),writable=False,readable=False),\n"
    s+="    Field('created_on','datetime',default=request.now,\n"
    s+="          label=T('Created On'),writable=False,readable=False),\n"
    s+="    Field('modified_on','datetime',default=request.now,\n"
    s+="          label=T('Modified On'),writable=False,readable=False,\n"
    s+="          update=request.now),\n"
    if not table=='auth_user' and 'auth_user' in session.app['tables']:
        s+="    Field('created_by',db.auth_user,default=auth.user_id,\n"
        s+="          label=T('Created By'),writable=False,readable=False),\n"
        s+="    Field('modified_by',db.auth_user,default=auth.user_id,\n"
        s+="          label=T('Modified By'),writable=False,readable=False,\n"
        s+="          update=auth.user_id),\n"
    elif table=='auth_user':
        s+="    Field('registration_key',default='',\n"
        s+="          writable=False,readable=False),\n"
        s+="    Field('reset_password_key',default='',\n"
        s+="          writable=False,readable=False),\n"
        s+="    Field('registration_id',default='',\n"
        s+="          writable=False,readable=False),\n"
    s+="    format='%("+first_field+")s',\n"
    s+="    migrate=settings.migrate)\n\n"
    if table=='auth_user':
        s+="""
db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
"""
    else:
        s+="db.define_table('%s_archive',db.%s,Field('current_record','reference %s'))\n" % (table,table,table)
    return s


def fix_db(filename):
    params=dict(session.app['params'])
    content=open(filename,'rb').read()
    if 'auth_user' in session.app['tables']:
        auth_user = make_table('auth_user',session.app['table_auth_user'])
        content=content.replace('sqlite://storage.sqlite',
                                params['database_uri'])
        content=content.replace('auth.define_tables()',\
            auth_user+'auth.define_tables(migrate=settings.migrate)')
    content+="""
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
"""
    if params['login_method']=='janrain':
        content+="""
from gluon.contrib.login_methods.rpx_account import RPXAccount
auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request,
    api_key = settings.login_config.split(':')[-1],
    domain = settings.login_config.split(':')[0],
    url = "http://%s/%s/default/user/login" % (request.env.http_host,request.application))
"""
    open(filename,'wb').write(content)

def make_menu(pages):
    s="""
response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
"""
    for page in pages:
        if not page.endswith('_read') and \
                not page.endswith('_update') and \
                not page.endswith('_search') and \
                not page.startswith('_') and not page.startswith('error'):
            s+="    (T('%s'),URL('%s').xml()==URL().xml(),URL('%s'),[]),\n" % \
                (' '.join(x.capitalize() for x in page.split('_')),page,page)
    s+=']'
    return s

def make_page(page,contents):
    if 'auth_user' in session.app['tables'] and not page in ('index','error'):
        s="@auth.requires_login()\ndef %s():\n" % page
    else:
        s="def %s():\n" % page
    items=page.rsplit('_',1)
    if items[0] in session.app['tables'] and len(items)==2:
        t=items[0]
        if items[1]=='read':
            s+="    record = db.t_%s(request.args(0)) or redirect(URL('error'))\n" % t
            s+="    form=crud.read(db.t_%s,record)\n" % t
            s+="    return dict(form=form)\n\n"
        elif items[1]=='update':
            s+="    record = db.t_%s(request.args(0),active=True) or redirect(URL('error'))\n" % t
            s+="    form=crud.update(db.t_%s,record,next='%s_read/[id]',\n"  % (t,t)
            s+="                     ondelete=lambda form: redirect(URL('%s_select')),\n" % t
            s+="                     onaccept=crud.archive)\n"
            s+="    return dict(form=form)\n\n"
        elif items[1]=='create':
            s+="    form=crud.create(db.t_%s,next='%s_read/[id]')\n" % (t,t)
            s+="    return dict(form=form)\n\n"
        elif items[1]=='select':
            s+="    f,v=request.args(0),request.args(1)\n"
            s+="    try: query=f and db.t_%s[f]==v or db.t_%s\n" % (t,t)
            s+="    except: redirect(URL('error'))\n"
            s+="    rows=db(query)(db.t_%s.active==True).select()\n" % t
            s+="    return dict(rows=rows)\n\n"
        elif items[1]=='search':
            s+="    form, rows=crud.search(db.t_%s,query=db.t_%s.active==True)\n" % (t,t)
            s+="    return dict(form=form, rows=rows)\n\n"
        else:
            t=None
    else:
        t=None
    if not t:
        s+="    return dict()\n\n"
    return s

def make_view(page,contents):
    s="{{extend 'layout.html'}}\n\n"
    s+=str(MARKMIN(contents))
    items=page.rsplit('_',1)
    if items[0] in session.app['tables'] and len(items)==2:
        t=items[0]
        if items[1]=='read':
            s+="\n{{=A(T('edit %s'),_href=URL('%s_update',args=request.args(0)))}}\n<br/>\n"%(t,t)
            s+='\n{{=form}}\n'            
            s+="{{for t,f in db.t_%s._referenced_by:}}{{if not t[-8:]=='_archive':}}" % t        
            s+="[{{=A(t[2:],_href=URL('%s_select'%t[2:],args=(f,form.record.id)))}}]"
            s+='{{pass}}{{pass}}'
        elif items[1]=='create':
            s+="\n{{=A(T('select %s'),_href=URL('%s_select'))}}\n<br/>\n"%(t,t)
            s+='\n{{=form}}\n'
        elif items[1]=='update':
            s+="\n{{=A(T('show %s'),_href=URL('%s_read',args=request.args(0)))}}\n<br/>\n"%(t,t)
            s+='\n{{=form}}\n'
        elif items[1]=='select':
            s+="\n{{if request.args:}}<h3>{{=T('For %s #%s' % (request.args(0)[2:],request.args(1)))}}</h3>{{pass}}\n" 
            s+="\n{{=A(T('create new %s'),_href=URL('%s_create'))}}\n<br/>\n"%(t,t)
            s+="\n{{=A(T('search %s'),_href=URL('%s_search'))}}\n<br/>\n"%(t,t)
            s+="\n{{if rows:}}"
            s+="\n  {{headers=dict((str(k),k.label) for k in db.t_%s)}}" % t
            s+="\n  {{=SQLTABLE(rows,headers=headers)}}"
            s+="\n{{else:}}"
            s+="\n  {{=TAG.blockquote(T('No Data'))}}"
            s+="\n{{pass}}\n"
        elif items[1]=='search':
            s+="\n{{=A(T('create new %s'),_href=URL('%s_create'))}}\n<br/>\n"%(t,t)
            s+='\n{{=form}}\n'
            s+="\n{{if rows:}}"
            s+="\n  {{headers=dict((str(k),k.label) for k in db.t_%s)}}" % t
            s+="\n  {{=SQLTABLE(rows,headers=headers)}}"
            s+="\n{{else:}}"
            s+="\n  {{=TAG.blockquote(T('No Data'))}}"
            s+="\n{{pass}}\n"
    return s

def populate(tables):

    s = 'from gluon.contrib.populate import populate\n'
    s+= 'if not db(db.auth_user).count():\n'
    for table in tables:
        t=table=='auth_user' and 'auth_user' or 't_'+table
        s+="     populate(db.%s,100)\n" % t
    return s

def create(options):
    if DEMO_MODE:
        session.flash = T('disabled in demo mode')
        redirect(URL('default','step6'))
    params = dict(session.app['params'])
    app = session.app['name']
    app_create(app,request,force=True,key=params['security_key'])

    ### save metadata in newapp/wizard.metadata
    meta = os.path.join(request.folder,'..',app,'wizard.metadata')
    file=open(meta,'wb')
    pickle.dump(session.app,file)
    file.close()

    ### apply theme
    if options.apply_layout and params['layout_theme']!='Default':
        try:
            fn = 'web2py.plugin.layout_%s.w2p' % params['layout_theme']
            theme = urllib.urlopen(LAYOUTS_APP+'/static/plugin_layouts/plugins/'+fn)
            plugin_install(app, theme, request, fn)
        except: response.flash = T("unable to install there")
    
    ### write configuration file into newapp/models/0.py
    model = os.path.join(request.folder,'..',app,'models','0.py')
    file = open(model,'wb')
    file.write("from gluon.storage import Storage\n")
    file.write("settings = Storage()\n\n")
    file.write("settings.migrate = True\n")
    for key,value in session.app['params']:
        file.write("settings.%s = %s\n" % (key,repr(value)))
    file.close()

    ### write configuration file into newapp/models/menu.py
    if options.generate_menu:
        model = os.path.join(request.folder,'..',app,'models','menu.py')
        file = open(model,'wb')
        file.write(make_menu(session.app['pages']))
        file.close()

    ### customize the auth_user table
    model = os.path.join(request.folder,'..',app,'models','db.py')
    fix_db(model)

    ### create newapp/models/db_wizard.py
    if options.generate_model:
        model = os.path.join(request.folder,'..',app,'models','db_wizard.py')
        file = open(model,'wb')
        file.write('### we prepend t_ to tablenames and f_ to fieldnames for disambiguity\n\n')
        tables=sort_tables(session.app['tables'])
        for table in tables:
            if table=='auth_user': continue
            file.write(make_table(table,session.app['table_'+table]))
        file.close()

    model = os.path.join(request.folder,'..',app,
                         'models','db_wizard_populate.py')
    if os.path.exists(model): os.unlink(model)
    if options.populate_database:        
        file = open(model,'wb')
        file.write(populate(session.app['tables']))
        file.close()

    ### create newapp/controllers/default.py
    if options.generate_controller:
        controller = os.path.join(request.folder,'..',app,'controllers','default.py')
        file = open(controller,'wb')
        file.write("""# -*- coding: utf-8 -*- 
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
""")
        for page in session.app['pages']:
            file.write(make_page(page,session.app.get('page_'+page,'')))
        file.close()

    ### create newapp/views/default/*.html
    if options.generate_views:
        for page in session.app['pages']:
            view = os.path.join(request.folder,'..',app,'views','default',page+'.html')
            file = open(view,'wb')
            file.write(make_view(page,session.app.get('page_'+page,'')))
            file.close()

    if options.erase_database:
        path = os.path.join(request.folder,'..',app,'databases','*')
        for file in glob.glob(path): os.unlink(file)


