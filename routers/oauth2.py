import http
from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from config import schemas
from fastapi import status, HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    
    # copy the data
    to_encode = data.copy()

    # extract an expire date
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # update the copied data
    to_encode.update({"exp": expire})

    #create the jwt token
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    #return the jwt token
    return encode_jwt



def get_current_user(token: str = Depends(oauth2_scheme)):
    crendentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Invalid", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, crendentials_exception)


def verify_access_token(token: str, credentials_exceptions):
    
    try:
        # decode the jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user_id
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exceptions
        
        # validate the 'id' using the TokenData schemas
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions
    
    return token_data