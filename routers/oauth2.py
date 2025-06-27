import http
from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from requests import Session
from config import database, schemas
from fastapi import status, HTTPException
from config import models
from config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    
    # copy the data
    to_encode = data.copy()
    print(to_encode)

    # extract an expire date
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # update the copied data
    to_encode.update({"exp": expire})

    #create the jwt token
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    #return the jwt token
    return encode_jwt



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    crendentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate Invalid",
    headers={"WWW-Authenticate": "Bearer"})
    print("token before verification: ", token)

    token = verify_access_token(token, crendentials_exception)
    print("token: ", token)#  user_id
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user

# to verify the access token
def verify_access_token(token: str, credentials_exception):
    
    try:
        # decode the jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload: ", payload)

        # Extract the user_id
        user_id: str = payload.get('user_id')

        if user_id is None:
            raise credentials_exception
        
        # validate the 'id' using the TokenData schemas
        token_data = schemas.TokenData(id=user_id)
        
    except JWTError:
        raise credentials_exception
    
    #return the user_id
    return token_data