import uvicorn
import os
from fastapi import FastAPI
from authapi.routes.users_route import user_router

app = FastAPI()

app.include_router(user_router)

PORT = int(os.getenv('PORT'))

if __name__ == "__main__":
    uvicorn.run("authapi.main:app", host="0.0.0.0", port=PORT)
