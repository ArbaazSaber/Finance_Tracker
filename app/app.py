from fastapi import FastAPI
from apis import banks

app = FastAPI(title="Finance Tracker Automation")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app:app")