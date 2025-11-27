from fastapi import Depends
from app.db.session import get_session
from app.cache.redis_client import get_redis
from app.core.auth import get_current_user

# Use these as Depends in routers where needed
get_db = Depends(get_session)
get_redis_client = get_redis
get_current_active_user = Depends(get_current_user)
