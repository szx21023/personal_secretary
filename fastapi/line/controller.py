from fastapi import Header, HTTPException
from fastapi import APIRouter, Body, Request

from linebot.exceptions import InvalidSignatureError

from main import app

router = APIRouter(prefix=f"/webhook", tags=["webhook"])

@router.post("")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers['x-line-signature']
    try:
        app.state.line_bot.handler.handle(body.decode("utf-8"), signature)
    
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="chatbot handle body error.")
    
    return 'OK'