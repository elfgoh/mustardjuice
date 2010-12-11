# -*- coding: utf-8 -*- 
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
def index():
    return dict(user=auth.user.username)

def error():
    return dict()

@auth.requires_login()
def membership_contract_create():
    form=crud.create(db.t_membership_contract,next='membership_contract_read/[id]')
    return dict(form=form)

@auth.requires_login()
def membership_contract_read():
    record = db.t_membership_contract(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_membership_contract,record)
    return dict(form=form)

@auth.requires_login()
def membership_contract_update():
    record = db.t_membership_contract(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_membership_contract,record,next='membership_contract_read/[id]',
                     ondelete=lambda form: redirect(URL('membership_contract_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_login()
def membership_contract_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_membership_contract[f]==v or db.t_membership_contract
    except: redirect(URL('error'))
    rows=db(query)(db.t_membership_contract.active==True).select()
    return dict(rows=rows)

@auth.requires_login()
def membership_contract_search():
    form, rows=crud.search(db.t_membership_contract,query=db.t_membership_contract.active==True)
    return dict(form=form, rows=rows)

@auth.requires_login()
def payment_create():
    form=crud.create(db.t_payment,next='payment_read/[id]')
    return dict(form=form)

@auth.requires_login()
def payment_read():
    record = db.t_payment(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_payment,record)
    return dict(form=form)

@auth.requires_login()
def payment_update():
    record = db.t_payment(request.args(0),active=True) or redirect(URL('error'))
    form=crud.update(db.t_payment,record,next='payment_read/[id]',
                     ondelete=lambda form: redirect(URL('payment_select')),
                     onaccept=crud.archive)
    return dict(form=form)

@auth.requires_login()
def payment_select():
    f,v=request.args(0),request.args(1)
    try: query=f and db.t_payment[f]==v or db.t_payment
    except: redirect(URL('error'))
    rows=db(query)(db.t_payment.active==True).select()
    return dict(rows=rows)

@auth.requires_login()
def payment_search():
    form, rows=crud.search(db.t_payment,query=db.t_payment.active==True)
    return dict(form=form, rows=rows)

