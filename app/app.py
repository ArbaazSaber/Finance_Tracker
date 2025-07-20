from fastapi import FastAPI
from apis import banks, categories, tags

app = FastAPI(title="Finance Tracker Automation")

app.include_router(banks.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app:app")