from typing import Annotated
from datetime import datetime,timedelta,timezone
from fastapi import FastAPI, Request , Form , HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError

SECRET_KEY= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTY4ODAwMjQwMH0.M3kLfEaXToojPbxx2Vb7MxJhL4m0xP9Y4ZZ9e5k3QOo"
TOKEN_SECOND_EXP = 20

db_users = {
    "gregory" : {
        "id" : 0,
        "username" : "gregory",
        "password" : "12345#hash"
    },

    "melanie" : {
        "id" : 1,
        "username" : "melanie",
        "password" : "54321#hash"
    }
}

app = FastAPI()

jinja2_template = Jinja2Templates(directory="templates")

def get_user(username:str, db:list):

    if username in db:
        return db[username]
    
def authenticate_user(password:str, password_plane:str):

    password_clean=password.split("#")[0]
    if password_plane==password_clean :
        return True
    return False

def create_token(data:list):
    data_token= data.copy()
    data_token["exp"] = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_SECOND_EXP)
    token_jwt = jwt.encode(data_token, key=SECRET_KEY, algorithm="HS256")
    return token_jwt


@app.get("/", response_class=HTMLResponse)

def root(request: Request) :
    return  jinja2_template.TemplateResponse("index.html",{"request" : request})
    

@app.get("/users/dashboard", response_class=HTMLResponse)

def dashboard(request: Request) :
    return  jinja2_template.TemplateResponse("dashboard.html",{"request" : request})

@app.post("/users/login")

def login(username: Annotated[str,Form()],password: Annotated[str,Form()]):

    user_data = get_user(username,db_users)
    if user_data is None:
        raise  HTTPException(
            status_code=401,
            detail="No authorization"
        )
    
    
    if not authenticate_user(user_data["password"],password):
        raise  HTTPException(
            status_code=401,
            detail="No authorization"
        )
    
    token= create_token({"username": user_data["username"]})

    return token