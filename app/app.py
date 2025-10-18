from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis import banks, categories, category_targets, tags, users, tag_rules, accounts, transactions, bank_configs

app = FastAPI(title="Finance Tracker Automation")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(banks.router)
app.include_router(bank_configs.router)
app.include_router(categories.router)
app.include_router(category_targets.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(tag_rules.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ =="__main__":
    import uvicorn
    uvicorn.run("app:app")