from .config import OWNER_ID
from .database import is_whitelisted

async def is_authorized(user_id):
    if user_id == OWNER_ID:
        return True
    return await is_whitelisted(user_id)

def is_owner(user_id):
    return user_id == OWNER_ID
