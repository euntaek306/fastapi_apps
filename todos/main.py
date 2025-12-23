from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

# FastAPI() 객체 생성
app = FastAPI()

abs_path = os.path.dirname(os.path.realpath(__file__))
# print(abs_path)
# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory=f"static"), name="static")
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")


@app.get("/")
def home(request: Request):
    todo = 200
    title = "fastapi 기본 실습"
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "todos": todo,
                                       "title":title})