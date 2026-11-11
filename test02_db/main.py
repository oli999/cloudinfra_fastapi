
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text

from database import get_db
from sqlalchemy.orm import Session # 자동 import 가 안되면 수동 import 하기 

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 테스트로 get_db 를 import 해보자
# result = get_db # 함수 

@app.get("/", response_class=HTMLResponse)
def index(req: Request):
    return templates.TemplateResponse(
        request=req,
        name="index.html",
        context={
            "noticeList":["오후 일정이 시작되었습니다", "어쩌구...", "저쩌구..."]
        }
    )

@app.get("/member", response_class=HTMLResponse)
def getMembers(req: Request, db: Session = Depends(get_db)):
    # 실행할 sql 문 준비
    query = text("""
        SELECT num, name, addr
        FROM member
        ORDER BY num DESC
    """)
    
    # db 객체를 이용해서 회원 목록 얻어오기
    result = db.execute(query)
    # 회원 목록이 들어 있는 list type 이라고 생각하면 된다 
    members = result.fetchall() 
    # 응답하기
    return templates.TemplateResponse(
        request=req,
        name="member/list.html",
        context={
            "members":members
        }
    )

@app.get("/member/new", response_class=HTMLResponse)
def memberNew(req: Request):
    return templates.TemplateResponse(
        request=req, 
        name="member/new.html"
    )
