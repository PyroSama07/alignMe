from fastapi import FastAPI

app = FastAPI()

print("hola")

@app.get("/")
async def root():
    print("hello world")

print("helo")