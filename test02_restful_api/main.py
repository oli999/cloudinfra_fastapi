from fastapi import Depends, FastAPI, Form, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

app = FastAPI()

@app.get("/")
def index(req: Request):
    return {
        "noticeList": ["오후 일정이 시작되었습니다", "어쩌구...", "저쩌구..."]
    }

# ========================================================
# [RESTful API 변경 사항 요약]
# 1. URL은 동사(new, edit, delete)를 빼고 자원 이름(복수형: /members)으로 통일
# 2. 행위는 HTTP 메서드(GET, POST, PUT, DELETE)로 구분
# ========================================================

# 1. 목록 조회: GET /member -> GET /members
@app.get("/members")
def getMembers(req: Request, db: Session = Depends(get_db)):
    query = text("""
        SELECT num, name, addr
        FROM member
        ORDER BY num DESC
    """)
    result = db.execute(query)
    members = result.mappings().fetchall() 
    return {
        "members": members
    }

# (주의: REST API에서는 폼 화면(UI)을 달라는 전용 엔드포인트(/member/new)를 만들지 않으므로 해당 함수는 삭제했습니다.)

# 2. 정보 추가: POST /member/new -> POST /members
@app.post("/members")
def memberNew(req: Request, name: str = Form(...), addr: str = Form(...), db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO member
        (name, addr)
        VALUES(:name, :addr )
    """)
    db.execute(query, {"name":name, "addr":addr})
    db.commit() 
    
    return {
        "msg": f"{name} 님의 정보를 저장했습니다",
        "url": "/members" # 프론트엔드가 참고할 이동 경로
    }

# 3. 단건 조회 (기존 수정 폼 용도): GET /member/edit/{num} -> GET /members/{num}
@app.get("/members/{num}")
def getMember(req: Request, num: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT num, name, addr
        FROM member
        WHERE num=:num
    """)
    row = db.execute(query, {"num":num}).mappings().fetchone()
    
    return {
        "row": row
    }

# 4. 정보 수정: POST /member/edit/{num} -> PUT /members/{num}
@app.put("/members/{num}")
def memberEdit(req: Request, num: int, name: str = Form(...), addr: str = Form(...), db: Session = Depends(get_db)):
    query = text("""
        UPDATE member
        SET name=:name, addr=:addr
        WHERE num=:num
    """)
    db.execute(query, {"num":num, "name":name, "addr":addr})
    db.commit()
    
    return {
        "msg": f"{name} 님의 정보를 수정했습니다!",
        "url": "/members"
    }

# 5. 정보 삭제: GET /member/delete/{num} -> DELETE /members/{num}
@app.delete("/members/{num}") 
def deleteMember(num: int, db: Session = Depends(get_db)):
    query = text("""
        DELETE FROM member
        WHERE num=:num
    """)
    db.execute(query, {"num":num})
    db.commit()

    return {
        "msg": "삭제되었습니다.", 
        "url": "/members"
    }