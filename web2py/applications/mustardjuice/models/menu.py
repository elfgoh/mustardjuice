
response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
admin_menu = []

#hide the admin menu if user is not an admin
if auth.has_membership('admin'):
    admin_menu = [
        (T('Member Create'),URL('member_create').xml()==URL().xml(),URL('member_create'),[]),
        (T('Member Select'),URL('member_select').xml()==URL().xml(),URL('member_select'),[]),
        (T('Membership Contract Create'),URL('membership_contract_create').xml()==URL().xml(),URL('membership_contract_create'),[]),
        (T('Membership Contract Select'),URL('membership_contract_select').xml()==URL().xml(),URL('membership_contract_select'),[]),
        (T('Payment Create'),URL('payment_create').xml()==URL().xml(),URL('payment_create'),[]),
        (T('Payment Select'),URL('payment_select').xml()==URL().xml(),URL('payment_select'),[]),
        (T('Contract Type Create'),URL('contract_type_create').xml()==URL().xml(),URL('contract_type_create'),[]),
        (T('Contract Type Select'),URL('contract_type_select').xml()==URL().xml(),URL('contract_type_select'),[]),
    ]
    
response.menu = [
    (T('Index'),URL('index').xml()==URL().xml(),URL('index'),[]),    
] + admin_menu
