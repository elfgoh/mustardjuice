from gluon.contrib.populate import populate
if not db(db.auth_user).count():
     populate(db.auth_user,10)
     #populate(db.t_membership_contract,100)
     #populate(db.t_payment,10)
     populate(db.t_contract_type,10)
