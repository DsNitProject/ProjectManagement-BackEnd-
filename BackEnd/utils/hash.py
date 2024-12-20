from passlib.context import CryptContext

pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password:str):
        return pwd.hash(password)
    def verify(password:str, hashed_password:str):
        return pwd.verify(password, hashed_password)