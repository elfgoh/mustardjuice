### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
db.define_table('t_contract_type',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('view',_href=URL('contract_type_read',args=id)))),
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_fee', type='integer',
          label=T('Fee')),
    Field('active','boolean',default=True,
          label=T('Active'),writable=False,readable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False),
    Field('modified_by',db.auth_user,default=auth.user_id,
          label=T('Modified By'),writable=False,readable=False,
          update=auth.user_id),
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_contract_type_archive',db.t_contract_type,Field('current_record','reference t_contract_type'))

########################################
db.define_table('t_membership_contract',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('view',_href=URL('membership_contract_read',args=id)))),
    Field('f_member', type='reference auth_user',
          label=T('Member')),
    Field('f_start_date', type='date',
          label=T('Start Date')),
    Field('f_end_date', type='date',
          label=T('End Date')),
    Field('f_contract_type', type='reference t_contract_type',
          label=T('Contract Type')),
    Field('active','boolean',default=True,
          label=T('Active'),writable=False,readable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False),
    Field('modified_by',db.auth_user,default=auth.user_id,
          label=T('Modified By'),writable=False,readable=False,
          update=auth.user_id),
    format='%(f_member)s',
    migrate=settings.migrate)

db.define_table('t_membership_contract_archive',db.t_membership_contract,Field('current_record','reference t_membership_contract'))

########################################
db.define_table('t_payment',
    Field('id','id',
          represent=lambda id:SPAN(id,' ',A('view',_href=URL('payment_read',args=id)))),
    #Field('f_contract', type='reference t_membership_contract',
    #     label=T('Contract')),
    Field('f_member', type='reference auth_user',
          label=T('Member')),
    Field('f_amount', type='integer',
          label=T('Amount')),
    Field('active','boolean',default=True,
          label=T('Active'),writable=False,readable=False),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False),
    Field('modified_by',db.auth_user,default=auth.user_id,
          label=T('Modified By'),writable=False,readable=False,
          update=auth.user_id),
    format='%(f_contract)s',
    migrate=settings.migrate)

db.define_table('t_payment_archive',db.t_payment,Field('current_record','reference t_payment'))
