from fastapi import HTTPException, status
from sqlalchemy import select
from app.database.models import User
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.utils.jwt_token import generate_access_token

password_context = CryptContext(schemes="bcrypt", deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        self.model = model
        self.session = session

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    
    async def _add_user(self, data: dict):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"])
        )
        return await self._add(user)

    async def _generate_token(self, email, password) -> str:
        # Validate Credentials
        user = await self._get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller email not found"
            )
        
        if not password_context.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )
        
        return generate_access_token(data={
            "user": {
                "name": user.name,
                "id": str(user.id)
            }
        })

        
