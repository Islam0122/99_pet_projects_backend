from .models import User
from .database import async_session
from datetime import datetime
from sqlalchemy import select

async def update_user_activity(user_id: int, username: str):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(tg_id=user_id, username=username)
            session.add(user)
        else:
            user.last_activity = datetime.utcnow()

        await session.commit()