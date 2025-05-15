from fastapi import FastAPI, HTTPException
from app import crud
from pydantic import BaseModel, Field
from app.models import UPIBase, UPIUpdate, UPIResponse

app = FastAPI()

class UPI(BaseModel):
    name: str = Field(..., min_length=1)
    upi_id: str = Field(..., min_length=5)

@app.post("/upi/")
def create_user(upi: UPI):
    try:
        crud.create_upi(upi.name, upi.upi_id)
        return {"message": "UPI created successfully"}
    except Exception as e:
        print(f"Error in create_user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/upi/")
def read_upi():
    return crud.get_all_upi()


@app.put("/upi/{id}")
def update_user(id: int, upi: UPI):
    try:
        crud.update_upi(id, upi.name, upi.upi_id)
        return {"message": "UPI updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/upi/{id}")
def delete_user(id: int):
    try:
        crud.delete_upi(id)
        return {"message": "UPI deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
