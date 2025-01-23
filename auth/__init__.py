from datetime import datetime

from auth.dao import get_user, add_user
import jwt


#optimised one
def do_login(username: str, password: str) -> str:
    """Returns a jwt token if the username and password are correct"""
    user = get_user(username)
    if user is None:
        raise ValueError('User not found')
    if user['password'] != password:
        raise ValueError('Incorrect password')
    return str(jwt.encode({"sub": username, "exp": datetime.now().timestamp() + 36000}, 'secret', algorithm='HS256'))

def sign_up(username: str, password: str):
    user = get_user(username)
    if user is not None:
        raise ValueError('User already exists')
    add_user(username, password)

