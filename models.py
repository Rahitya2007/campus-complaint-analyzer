from pydantic import BaseModel


class Complaint(BaseModel):
    name: str
    email: str
    category: str
    complaint: str
    priority: str
    sentiment: str