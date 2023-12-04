from fastapi import FastAPI,Request,Form
from camera import start_camera
from pydantic import BaseModel
import uvicorn
import oracledb
from dotenv import load_dotenv
import os
import json
import pandas as pd
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


templates = Jinja2Templates(directory="Frontend")



load_dotenv()

def connect_db():
    connection = oracledb.connect(
        user=os.getenv("SQL_USERNAME"),
        password=os.getenv("SQL_PASSWORD"),
        dsn=os.getenv("SQL_DSN"))
    connection.autocommit = True
    print("connected to oracle database")
    cursor = connection.cursor()
    return(connection,cursor)

connection,cursor = connect_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html = True), name="static")

origins = ["*"]
app.add_middleware(CORSMiddleware,allow_origins = origins,
                   allow_methods = ["*"],
                   allow_credentials = True,
                   allow_headers = ["*"])

@app.get("/")
async def root(request:Request):
    # return {"message": "Hello World"}
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/loginz")
async def root(request:Request):
    # return {"message": "Hello World"}
    return templates.TemplateResponse("login.html",{"request":request})

class Exercise(BaseModel):
    exercise_name: str=Form(...)

class SignUp(BaseModel):
    email: str
    name: str
    password: str
    contact: int

class LogIn(BaseModel):
    email: str
    password: str

@app.post("/exercise")
async def stream_exercise(req: Request,exercise_name:str=Form(...)):
    # print(data)
    # request=data.exercise_name
    try:
        selected_exercise = exercise_name
        obj = start_camera(selected_exercise)
        return templates.TemplateResponse("exercise.html",{"request":req})
        # return {"count":obj}
    except Exception as e:
        print(e)

def valid_email(email,connection):
    query = "select * from users where email = '{}'".format(email)
    atr = '@' in email
    if pd.read_sql(query,connection).shape[0]==0:
        return atr
    else:
        return False

@app.post("/signup")
async def signup(request: Request,name:str=Form(...),email:str=Form(...),password:str=Form(...),contact:int=Form(...)):
    if valid_email(email,connection):
        try:
            cursor.execute("insert into users (email,name,password,contact) values ('{}','{}','{}','{}')".
                    format(email,name,password,contact))
            return {"Status",'Acoount Created'}
        except Exception as e:
            return {"Status","{}".format(e)}
    else:
        return{"Status","Email not valid or Already exists"}

@app.post("/login")
async def login(request: Request,email:str=Form(...),password:str=Form(...)):

    query_pass = "SELECT password FROM users WHERE email = '{}'".format(email)
    valid_email = pd.read_sql(query_pass,connection).shape[0]
    if valid_email:
        query_pass = "SELECT password FROM users WHERE email = '{}'".format(email)
        df = pd.read_sql(query_pass,connection)
        auth_pass = df.iloc[0][0]
        if auth_pass == password:
            # return {"Status","Access Granted"}
            return templates.TemplateResponse("exercise.html",{"request":request})
        
        else:
            # return templates.TemplateResponse("index.html",{"request":request})
            # return RedirectResponse(url="http://127.0.0.1:5500/")
            return {"Status","Access Not Granted. Press back to return!"}
    else:
        return {"Status","E-Mail Doesnt Exist"}


if __name__ == "__main__":
    uvicorn.run("app:app",reload = True,host="127.0.0.1",port=1300)
