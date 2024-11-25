from typing import Annotated
from fastapi import FastAPI, Request , Form , HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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
    
    return {
        "username":username,
        "password":password
        }