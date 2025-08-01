from fastapi import FastAPI
from apis import banks, categories, tags, users, tag_rules, accounts

app = FastAPI(title="Finance Tracker Automation")

app.include_router(banks.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(tag_rules.router)
app.include_router(accounts.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app:app")