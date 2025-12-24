from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse, JSONResponse
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from pydantic import BaseModel, Field
import os

# API key 로딩
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# FastAPI() 객체 생성
app = FastAPI()

abs_path = os.path.dirname(os.path.realpath(__file__))
# print(abs_path)
# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")


# 1. 출력 스키마 정의
class JobDescOutput(BaseModel):
    job_role: str = Field(description="직군명")
    level: str = Field(description="숙련도 수준")
    core_skills: list[str] = Field(description="핵심 기술 역량")
    tools: list[str] = Field(description="필수 도구 및 기술 스택")
    soft_skills: list[str] = Field(description="비기술 역량")
    describe: str = Field(description="직업 설명")

# 2. LangChain 구성
parser = JsonOutputParser(pydantic_object=JobDescOutput)

prompt = PromptTemplate(
    template="""
    당신은 IT 취업 컨설턴트입니다.
    아래 입력을 바탕으로 직무 설명(Job Description)을 생성하세요.

    직군: {job_role}
    숙련도: {level}

    {format_instructions}
    """,
    input_variables=["job_role", "level"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0.3
)

chain = prompt | llm | parser


# 3. 화면 렌더링
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 4.Job Description 생성 API
@app.post("/generate")
def generate_job_desc(request: Request,
                      job_role: str = Form(...), 
                      level: str = Form(...)):
    input_data = {
        "job_role": job_role,
        "level": level
    }
    print("요청시작")
    result = chain.invoke(input_data)
    print("요청완료")

    # 🔑 여기서 한글 유지
    import json
    result_json = json.dumps(result, ensure_ascii=False, indent=2)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "job_role": job_role,
            "level": level
        }
    )