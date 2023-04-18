from fastapi import FastAPI
from camera import start_camera
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Exercise(BaseModel):
    exercise_name: str

@app.post("/")
async def stream_exercise(request: Exercise):
    try:
        selected_exercise = request.exercise_name
        obj = start_camera(selected_exercise)
        return {"count":obj}
    except Exception as e:
        print(e)

if __name__ == "__main__":
    uvicorn.run("app:app",reload = True,host="127.0.0.1",port=1300)