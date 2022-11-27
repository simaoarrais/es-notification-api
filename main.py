import src.sms_notification as sms_notification
import src.wpp_notification as wpp_notification
import src.call_notification as call_notification

import json

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

class Notification(BaseModel):
    phone_number: str
    message: str

app = FastAPI()

@app.get("/sms")
async def sms(body: Notification):
    body_json = json.dumps(body.dict())
    sid = sms_notification.send_notification(body_json)
    return sid

@app.get("/wpp")
async def wpp(body: Notification):
    body_json = json.dumps(body.dict())
    sid = wpp_notification.send_notification(body_json)
    return sid

@app.get("/call")
async def call(body: Notification):
    body_json = json.dumps(body.dict())
    sid = call_notification.send_notification(body_json)
    return sid
