from fastapi import FastAPI

APP = FastAPI()
API = FastAPI()
VIEW = FastAPI()
APP.mount("/api", API)
APP.mount("/view", VIEW)

__all__ = ["APP"]
