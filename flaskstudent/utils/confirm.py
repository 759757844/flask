from functools import wraps
from flask import session,redirect
def decorator(f):
    @wraps(f)
    def dec(*args,**kwargs):
        user = session.get('user')
        if user:
            return f(*args,**kwargs)
        else:
            return redirect('/user/login')
    return dec