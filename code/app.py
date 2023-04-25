from fastapi import FastAPI
from camera import start_camera
from pydantic import BaseModel
import uvicorn
import getpass
import oracledb
from dotenv import load_dotenv
import os
import pandas as pd


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

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Exercise(BaseModel):
    exercise_name: str

class SignUp(BaseModel):
    email: str
    name: str
    password: str
    contact: int

class LogIn(BaseModel):
    email: str
    password: str

@app.post("/")
async def stream_exercise(request: Exercise):
    try:
        selected_exercise = request.exercise_name
        obj = start_camera(selected_exercise)
        return {"count":obj}
    except Exception as e:
        print(e)

def valid_email(email,connection):
    query = "select * from users where email = '{}'".format(email)
    atr = '@' in email
    if pd.read_sql(query,connection).shape[0]==0:
        return atr
    else:
        return False

@app.post("/register/")
async def signup(request: SignUp):
    if valid_email(request.email,connection):
        try:
            cursor.execute("insert into users (email,name,password,contact) values ('{}','{}','{}','{}')".
                    format(request.email,request.name,request.password,request.contact))
            return {"Status",'Acoount Created'}
        except Exception as e:
            return {"Status","{}".format(e)}
    else:
        return{"Status","Email not valid or Already exists"}

@app.post("/regiter/")
async def login(request: LogIn):
    query_pass = "SELECT password FROM users WHERE email = '{}'".format(request.email)
    valid_email = pd.read_sql(query_pass,connection).shape[0]
    if valid_email:
        query_pass = "SELECT password FROM users WHERE email = '{}'".format(request.email)
        df = pd.read_sql(query_pass,connection)
        auth_pass = df.iloc[0][0]
        if auth_pass == request.password:
            return {"Status","Access Granted"}
        else:
            return {"Status","Access Not Granted"}
    else:
        return {"Status","E-Mail Doesnt Exist"}


if __name__ == "__main__":
    uvicorn.run("app:app",reload = True,host="127.0.0.1",port=1300)