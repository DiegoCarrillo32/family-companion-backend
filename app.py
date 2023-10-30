from init_db import Database
import queries
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = Database(host="localhost",
                database="family_db",
                user="postgres",
                password="2409")


# Si no tiene las tablas creadas en su local, corra el siguiente comando.
conn.create_tables()


@app.route('/register_user', methods=['POST'])
def register_user():
    content = request.json
    print(content["user_id"])
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


@app.route('/register_family_member', methods=['POST'])
def register_family_member():
    content = request.json
    if content["family_user_chatId"] is None and content["user_mode"] not in ["F"]:
        return jsonify({
            "error": "Invalid data"
        })

    query = queries.GET_USER_BY_CHAT_ID(content["family_user_chatId"])
    conn.cur.execute(query)
    user = conn.cur.fetchone()
    if user is None:
        return jsonify({
            "error": "User not found"
        })

    query = queries.INSERT_FAMILY_MEMBER(content["family_user_chatId"], user[3])
    conn.cur.execute(query)
    user_id = conn.cur.fetchone()[0]
    conn.conn.commit()
    return jsonify({
        "user_id": user_id,
        "user_mode": "F",
        "family_user_chatId": content["family_user_chatId"]
    })


@app.route('/detected_face')
def detected_face():
    # LLamen todos los miembros.family_user_chatId
    # Por cada miembro, manden el mensaje

    pass


if __name__ == '__main__':
    app.run()
