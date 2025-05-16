from pydantic import BaseModel


class UPIBase(BaseModel):
    name: str
    upi_id: str


class UPIUpdate(BaseModel):
    name: str


class UPIResponse(UPIBase):
    id: int
