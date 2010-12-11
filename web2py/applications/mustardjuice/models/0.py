from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Mustardjuice club membership fees management system'
settings.subtitle = 'powered by web2py'
settings.author = 'elfgoh'
settings.author_email = 'elfgoh@yahoo.com'
settings.keywords = ''
settings.description = "Manage your club's memberhship fees."
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '3d9993b8-c012-4db8-9377-1c2c4fc65e2b'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = 'elfgoh@yahoo.com'
settings.login_method = 'local'
settings.login_config = ''
