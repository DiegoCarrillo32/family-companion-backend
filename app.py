from datetime import datetime

import requests
from bot_configuration import TOKEN
from init_db import Database
import queries
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = Database(host="localhost",
                database="family_db",
                user="postgres",
                password="1234")

# Si no tiene las tablas creadas y la función en su local, corra los siguientes comandos.
conn.create_tables()
conn.function_check_emotions_and_clear()


# {
#	"family_user_chatId": "123456789",
#	"user_mode": "A"
# }

@app.route('/register_user', methods=['POST'])
def register_user():
    content = request.json
    # print(content["user_id"])
    # Validate the fields
    if content["user_mode"] not in ["A"] and content["family_user_chatId"] is None:
        return jsonify({
            "error": "Invalid user_mode"
        })
    query = queries.INSERT_ADMIN_USER(content["user_mode"], content["family_user_chatId"])
    conn.cur.execute(query)
    user_id = conn.cur.fetchone()[0]
    conn.conn.commit()
    print(user_id)
    return jsonify({
        "user_id": user_id,
        "user_mode": content["user_mode"],
        "family_user_chatId": content["family_user_chatId"]
    })


# {
#	"family_user_chatId": "123456789",
#	"family_member_chatId":"1111448781",
#	"user_mode": "F"
# }

@app.route('/register_family_member', methods=['POST'])
def register_family_member():
    content = request.json
    if content["family_user_chatId"] is None and content["user_mode"] not in ["F"]:
        return jsonify({
            "error": "Invalid data"
        })

    query = queries.GET_USER_BY_CHAT_ID(content["family_user_chatId"])  # admin
    conn.cur.execute(query)
    user = conn.cur.fetchone()
    if user is None:
        return jsonify({
            "error": "User not found"
        })

    query = queries.INSERT_FAMILY_MEMBER(content["family_member_chatId"], user[3])
    conn.cur.execute(query)
    user_id = conn.cur.fetchone()[0]
    conn.conn.commit()
    return jsonify({
        "user_id": user_id,
        "user_mode": "F",
        "family_user_chatId": content["family_member_chatId"]
    })


# {
#   family_user_chatId: "123456789",
#   joy_emotion : "",
#   sorrow_emotion:"",
#   anger_emotion :"",
#   surprise_emotion:""
# }
'''SAMPLE DATA
{
    "family_user_chatId": "1362991318",
    "joy": "very likely",
    "sorrow": "very likely",
    "anger": "very likely",
    "surprise": "very likely"
}
'''


@app.route('/detected_face', methods=['POST'])
def detected_face():
    # validate the fields above
    content = request.json
    query = queries.GET_USER_BY_CHAT_ID(content["family_user_chatId"])
    conn.cur.execute(query)
    user = conn.cur.fetchone()
    if user is None:
        return jsonify({
            "error": "User not found"
        })

    print(user)

    #fecha
    date = datetime.now()
    #enviar a la base de datos
    query = queries.INSERT_DETECTION_LOG(date, user[3], content["joy"], content["sorrow"],
                                         content["anger"], content["surprise"])
    # print(query)
    conn.cur.execute(query)
    conn.conn.commit()

    #invocar la funcion de postgres
    query = queries.CHECK_EMOTIONS_AND_CLEAR(user[3])
    conn.cur.execute(query)
    results = conn.cur.fetchall()

    #sino esta vacio se envia el mensaje
    if len(results) != 0:
        conn.conn.commit()
        text = ''
        for result in results:
            text += f' {result[1]}: {result[2]}\n'
        #se recupera el chatid del groupid
        query = queries.GET_CHAT_ID_BY_FAMILY_GROUP_ID(user[3])
        conn.cur.execute(query)
        family_members = conn.cur.fetchall()
        #se envia el mensaje cada uno de los miembros
        for member in family_members:
            print(member)
            family_member = member[0]

            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={family_member}&text={text}'
            # url = f'https://api.telegram.org/bot6801162244:AAFfKg3o-ThaHmSkwYcI7M6VNxaXaQNNoHk/sendMessage?chat_id=1362991318&text=algo'
            response = requests.post(url)
            print(response.content)
    return jsonify({
        "message": "Success"
    })





if __name__ == '__main__':
    app.run()
