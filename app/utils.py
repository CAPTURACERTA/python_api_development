from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
"""
this is not being used nowadays btw
I had to do "uv add bcrypt==3.2.2" to donwload the version fastapi
tutorials used to use to work...
"""
# 
# 

def hash(password: str):
    return pwd_context.hash(password)