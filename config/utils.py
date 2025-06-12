from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_method(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):

    # this coverts thr plain password to hashed codes and then compare both hashed password
    return pwd_context.verify(plain_password, hashed_password)