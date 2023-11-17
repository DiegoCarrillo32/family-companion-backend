import uuid

# Query to insert or register the admin user, it gets the user mode, the admin chat ID and create the family user chat ID
def INSERT_ADMIN_USER(user_mode, family_user_chatId):
    return f"""
        INSERT INTO users (user_id, user_mode, family_user_chatId)
        VALUES ('{str(uuid.uuid4())}', '{user_mode}', '{family_user_chatId}')
        RETURNING user_id;
    """

# Query to get an user by the chat id
def GET_USER_BY_CHAT_ID(chat_id):
    return f"""
        SELECT user_id, user_mode, family_user_chatId , family_group_id
        FROM users 
        WHERE family_user_chatId = '{chat_id}';
    """

# Query to inser a family member it gets the family chat ID and the user chat ID
def INSERT_FAMILY_MEMBER( family_user_chatId, family_group_id):
    return f"""
        INSERT INTO users (user_id, user_mode, family_user_chatId, family_group_id)
        VALUES ('{str(uuid.uuid4())}', 'F', '{family_user_chatId}', '{family_group_id}')
        RETURNING user_id;
    """

# Query to obtain a chat ID from the group id
def GET_CHAT_ID_BY_FAMILY_GROUP_ID(family_group_id):
    return f"""
        SELECT family_user_chatId
        FROM users 
        WHERE family_group_id = '{family_group_id}';
    """


# Query to insert the results obtained from the Google Vision service
def INSERT_DETECTION_LOG(detection_date, family_group_id, joy_emotion, sorrow_emotion, anger_emotion, surprise_emotion):
    return f"""
        INSERT INTO detection_log (detection_date, joy_emotion, sorrow_emotion, anger_emotion, surprise_emotion, family_group_id)
        VALUES ('{detection_date}', '{joy_emotion}', '{sorrow_emotion}', '{anger_emotion}', '{surprise_emotion}', '{family_group_id}')
    """

# Get all rows from the detection log
def GET_DETECTION_LOG():
    return f"""
        SELECT * FROM detection_log
    """


def CHECK_EMOTIONS_AND_CLEAR(family_group_id):
    return f"""
    SELECT * FROM check_emotions_and_clear('{family_group_id}');
    """