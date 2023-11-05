import psycopg2


class Database:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(255) PRIMARY KEY,
                user_mode CHAR(1) NOT NULL,
                family_user_chatId VARCHAR(255) NOT NULL,
                family_group_id UUID DEFAULT uuid_generate_v4()
            );
        """)

        self.cur.execute("""
                  CREATE TABLE IF NOT EXISTS detection_log (
                      dect_log SERIAL PRIMARY KEY,
                      detection_date DATE NOT NULL,
                      joy_emotion VARCHAR(255) NOT NULL,
                      sorrow_emotion VARCHAR(255) NOT NULL,
                      anger_emotion VARCHAR(255) NOT NULL,
                      surprise_emotion VARCHAR(255) NOT NULL,   
                      family_group_id UUID NOT NULL
                  );
              """)

        self.conn.commit()

    def drop_tables(self):
        self.cur.execute("""
            DROP TABLE IF EXISTS users;
        """)

        self.cur.execute("""
            DROP TABLE IF EXISTS detection_log;
        """)

        self.conn.commit()

    def close(self):
        self.conn.close()
