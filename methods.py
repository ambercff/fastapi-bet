import jwt

SECRET_KEY = "caio-amber"
ALGORITHM = "HS256"

def create_access_token(username : str):
    
        to_encode = {"sub": username}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
        
        return encoded_jwt

def decode_access_token(token: str):
    
    decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    
    return decoded
