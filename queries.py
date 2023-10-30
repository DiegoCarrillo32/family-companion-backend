import uuid


def INSERT_ADMIN_USER(user_mode, family_user_chatId):
    return f"""
        INSERT INTO users (user_id, user_mode, family_user_chatId)
        VALUES ('{str(uuid.uuid4())}', '{user_mode}', '{family_user_chatId}')
        RETURNING user_id;
    """

def GET_USER_BY_CHAT_ID(chat_id):
    return f"""
        SELECT user_id, user_mode, family_user_chatId , family_group_id
        FROM users 
        WHERE family_user_chatId = '{chat_id}';
    """

def INSERT_FAMILY_MEMBER( family_user_chatId, family_group_id):
    return f"""
        INSERT INTO users (user_id, user_mode, family_user_chatId, family_group_id)
        VALUES ('{str(uuid.uuid4())}', 'F', '{family_user_chatId}', '{family_group_id}')
        RETURNING user_id;
    """