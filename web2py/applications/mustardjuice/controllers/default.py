# -*- coding: utf-8 -*- 
### required - do no delete

import datetime

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires

@auth.requires_login()
def index():
    #check if user has any contracts
    contract_rows = db(db.t_membership_contract.f_member == auth.user.id).select()

    #check if user has any payments
    payment_rows = db(db.t_payment.f_member == auth.user.id).select()
    
    total_credit, total_debit, i= 0, 0, 0
    
    for row in payment_rows:
        total_credit += row.f_amount
    
    for row in contract_rows:
        if row.f_end_date == None:
            end_date = datetime.date.today()
        
        #calculating months that have passed in the contract
        m1 = end_date.month + end_date.year*12
        m2 = row.f_start_date.month + row.f_start_date.year*12
        contract_rows[i].months_passed = m1 - m2
        
        #calculate sum consumed based on time elapsed for contract
        contract_rows[i].debit = contract_rows[i].months_passed * contract_rows[i].f_contract_type.f_fee
        
        total_debit += contract_rows[i].debit
        
        i+=1    
        
        
    return dict(user=auth.user.username, contract_rows=contract_rows, payment_rows=payment_rows, total_debit=total_debit, total_credit=total_credit )

def error():
    return dict()

@auth.requires_membership('admin')
def member_create():
    form=crud.create(db.auth_user,next='member_read/[id]')
    return dict(form=form)

@auth.requires_membership('admin')
def member_read():
    record = db.auth_user(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.auth_user,record)
    return dict(form=form)
 
@auth.requires_membership('admin')
def member_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.auth_user[f]==v or db.auth_user
    except: redirect(URL('error'))
    rows=db(query)(db.auth_user.id>0).select()
    return dict(rows=rows)

@auth.requires_membership('admin')
def member_search():
    form, rows=crud.search(db.auth_user)
    return dict(form=form, rows=rows)

@auth.requires_membership('admin')
def member_update():
    record = db.auth_user(request.args(0)) or redirect(URL('error'))
    form=crud.update(db.auth_user,record,next='member_read/[id]',
                     ondelete=lambda form: redirect(URL('member_select'))
                     )
    return dict(form=form)
   
@auth.requires_membership('admin')
def membership_contract_create():
    form=crud.create(db.t_membership_contract,next='membership_contract_read/[id]')
    return dict(form=form)

@auth.requires_membership('admin')
def membership_contract_read():
    record = db.t_membership_contract(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_membership_contract,record)
    return dict(form=form)

@auth.requires_membership('admin')
def membership_contract_update():
    record = db.t_membership_contract(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_membership_contract,record,next='membership_contract_read/[id]',
                     ondelete=lambda form: redirect(URL('membership_contract_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_membership('admin')
def membership_contract_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_membership_contract[f]==v or db.t_membership_contract
    except: redirect(URL('error'))
    rows=db(query)(db.t_membership_contract.active==True).select()
    return dict(rows=rows)

@auth.requires_membership('admin')
def membership_contract_search():
    form, rows=crud.search(db.t_membership_contract,query=db.t_membership_contract.active==True)
    return dict(form=form, rows=rows)

@auth.requires_membership('admin')
def payment_create():
    form=crud.create(db.t_payment,next='payment_read/[id]')
    return dict(form=form)

@auth.requires_membership('admin')
def payment_read():
    record = db.t_payment(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_payment,record)
    return dict(form=form)

@auth.requires_membership('admin')
def payment_update():
    record = db.t_payment(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_payment,record,next='payment_read/[id]',
                     ondelete=lambda form: redirect(URL('payment_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_membership('admin')
def payment_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_payment[f]==v or db.t_payment
    except: redirect(URL('error'))
    rows=db(query)(db.t_payment.active==True).select()
    return dict(rows=rows)

@auth.requires_membership('admin')
def payment_search():
    form, rows=crud.search(db.t_payment,query=db.t_payment.active==True)
    return dict(form=form, rows=rows)

@auth.requires_membership('admin')
def contract_type_create():
    form=crud.create(db.t_contract_type,next='contract_type_read/[id]')
    return dict(form=form)

@auth.requires_membership('admin')
def contract_type_read():
    record = db.t_contract_type(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_contract_type,record)
    return dict(form=form)

@auth.requires_membership('admin')
def contract_type_update():
    record = db.t_contract_type(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_contract_type,record,next='contract_type_read/[id]',
                     ondelete=lambda form: redirect(URL('contract_type_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_membership('admin')
def contract_type_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_contract_type[f]==v or db.t_contract_type
    except: redirect(URL('error'))
    rows=db(query)(db.t_contract_type.active==True).select()
    return dict(rows=rows)

@auth.requires_membership('admin')
def contract_type_search():
    form, rows=crud.search(db.t_contract_type,query=db.t_contract_type.active==True)
    return dict(form=form, rows=rows)