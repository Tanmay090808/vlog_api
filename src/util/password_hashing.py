from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['pbkdf2_sha256'],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_hash_password(plain_password:str , hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)