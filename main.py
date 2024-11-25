from typing import Annotated
from fastapi import FastAPI, Request , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

jinja2_template = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)

def root(request: Request) :
    return  jinja2_template.TemplateResponse("index.html",{"request" : request})
    

@app.get("/users/dashboard", response_class=HTMLResponse)

def dashboard(request: Request) :
    return  jinja2_template.TemplateResponse("dashboard.html",{"request" : request})

@app.post("/users/login")

def login(username: Annotated[str,Form()],password: Annotated[str,Form()]):
    return {
        "username":username,
        "password":password
        }