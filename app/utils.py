from passlib.context import CryptContext

#define the hashing algorithm (bcrypt) for securing passwords in the database
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)