import os, time, json, jwt, asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncpg
from pydantic import BaseModel
from bcrypt import hashpw, gensalt, checkpw

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
SECRET = os.getenv("SECRET_KEY")

DSN = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)

# — Models —
class Token(BaseModel):
    access_token: str
    token_type: str

class ReportReq(BaseModel):
    meter_id: int
    tipo: str  # 'estadistica'|'tendencia'|'factor_carga'|'normativa'
    programado: bool = False

# — Helpers —
async def get_conn():
    return await asyncpg.connect(DSN)

async def authenticate(user, pwd):
    conn = await get_conn()
    row = await conn.fetchrow("SELECT * FROM users WHERE username=$1", user)
    await conn.close()
    if row and checkpw(pwd.encode(), row['password_hash'].encode()):
        return row
    return None

async def current_user(token=Depends(oauth2)):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data
    except:
        raise HTTPException(401, "Token inválido")

# — Auth Endpoints —
@app.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(form.username, form.password)
    if not user:
        raise HTTPException(400, "Credenciales inválidas")
    payload = {"sub": user['username'], "user_id": user['id'], "exp": time.time()+3600}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# — WebSocket Realtime —
@app.websocket("/ws/realtime")
async def ws_realtime(ws: WebSocket, user=Depends(current_user)):
    await ws.accept()
    conn = await asyncpg.connect(DSN)
    try:
        while True:
            row = await conn.fetchrow("""
              SELECT ts, vals
              FROM raw_readings
              ORDER BY ts DESC LIMIT 1
            """)
            await ws.send_json(dict(row))
            await asyncio.sleep(2)
    finally:
        await conn.close()

# — History & Stats —
@app.get("/api/history")
async def history(period: str = "1h", user=Depends(current_user)):
    conn = await asyncpg.connect(DSN)
    rows = await conn.fetch(f"""
        SELECT ts, avg
        FROM minute_stats
        WHERE ts > now() - interval '{period}'
        ORDER BY ts
    """)
    await conn.close()
    return [dict(r) for r in rows]

@app.get("/api/stats")
async def stats(window: int = 60, user=Depends(current_user)):
    conn = await asyncpg.connect(DSN)
    row = await conn.fetchrow(f"""
      SELECT MIN(avg), MAX(avg), AVG(avg)
      FROM minute_stats WHERE ts > now() - interval '{window} seconds'
    """)
    await conn.close()
    return {"min": row[0], "max": row[1], "avg": row[2]}

# — Report Requests —
@app.post("/api/report")
async def create_report(req: ReportReq, user=Depends(current_user)):
    conn = await asyncpg.connect(DSN)
    await conn.execute("""
      INSERT INTO report_requests(meter_id,tipo,status,programado)
      VALUES($1,$2,'pending',$3)
    """, req.meter_id, req.tipo, req.programado)
    await conn.close()
    return {"ok": True}
