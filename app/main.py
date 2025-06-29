from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

from app import crud

app = FastAPI()


class UPI(BaseModel):
    name: str = Field(..., min_length=1)
    upi_id: str = Field(..., min_length=5)


@app.post("/upi/")
def create_user(upi: UPI) -> dict:
    try:
        crud.create_upi(upi.name, upi.upi_id)
        return {"message": "UPI created successfully"}
    except Exception as e:
        logger.error(f"Error in create_user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/upi/")
def read_upi() -> list:
    return crud.get_all_upi()


@app.put("/upi/{id}")
def update_user(id: int, upi: UPI) -> dict:
    try:
        crud.update_upi(id, upi.name, upi.upi_id)
        return {"message": "UPI updated successfully"}
    except Exception as e:
        logger.error(f"Error in update_user: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
@app.delete("/upi/{id}")
def delete_user(id: int) -> dict:
    try:
        crud.delete_upi(id)
        return {"message": "UPI deleted successfully"}
    except Exception as e:
        logger.error(f"Error in delete_user: {e}")
        raise HTTPException(status_code=400, detail=str(e))
