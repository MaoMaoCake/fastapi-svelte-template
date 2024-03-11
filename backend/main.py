from fastapi import FastAPI

from auth.routes import authRouter

app = FastAPI()

app.include_router(authRouter)


