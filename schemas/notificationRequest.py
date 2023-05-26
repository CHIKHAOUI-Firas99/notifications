from pydantic import BaseModel

class NotificationRequest(BaseModel):
    des: str
