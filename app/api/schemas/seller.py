from pydantic import BaseModel, EmailStr

class BaseSeller(BaseModel):
    name: str
    email: EmailStr
    address: str
    zip_code: int

class SellerCreate(BaseSeller):
    password: str

class SellerRead(BaseSeller):
    pass