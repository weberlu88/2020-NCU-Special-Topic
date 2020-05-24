from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username, password):
    user = user.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    userid = payload['identity']
    return user.find_by_id(userid)