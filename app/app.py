from fastapi import FastAPI
from apis import banks, tags

app = FastAPI(title="Finance Tracker Automation")

app.include_router(banks.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app:app")