from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_mapping = {u.username: u for u in users}
userid_mapping   = {u.id: u for u in users}

# 驗證身分正確的方法，回傳jwt token
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

# Auth Endpoint
def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid, None)