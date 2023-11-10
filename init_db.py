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

    def function_check_emotions_and_clear(self):
        self.cur.execute("""
        CREATE OR REPLACE FUNCTION check_emotions_and_clear()
        RETURNS TABLE(emotion VARCHAR, status VARCHAR, recommendation VARCHAR) AS $$
        DECLARE
            joy_count INT;
            sorrow_count INT;
            anger_count INT;
            surprise_count INT;
        BEGIN
            SELECT COUNT(*) INTO joy_count FROM detection_log WHERE joy_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO sorrow_count FROM detection_log WHERE sorrow_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO anger_count FROM detection_log WHERE anger_emotion IN ('Very Likely', 'Likely');
            SELECT COUNT(*) INTO surprise_count FROM detection_log WHERE surprise_emotion IN ('Very Likely', 'Likely');
            
            IF joy_count > 5 THEN
                RETURN QUERY SELECT 'Joy'::VARCHAR, 'High Joy Detected'::VARCHAR, 'Keep up the positive environment!'::VARCHAR;
            ELSIF sorrow_count > 5 THEN
                RETURN QUERY SELECT 'Sorrow'::VARCHAR, 'High Sorrow Detected'::VARCHAR, 'Consider providing support and care.'::VARCHAR;
            ELSIF anger_count > 5 THEN
                RETURN QUERY SELECT 'Anger'::VARCHAR, 'High Anger Detected'::VARCHAR, 'Engage in calming activities and conflict resolution.'::VARCHAR;
            ELSIF surprise_count > 5 THEN
                RETURN QUERY SELECT 'Surprise'::VARCHAR, 'High Surprise Detected'::VARCHAR, 'Ensure the surprises are pleasant, or provide stability.'::VARCHAR;
            END IF;

            -- Vaciar la tabla después de devolver el mensaje.
            TRUNCATE TABLE detection_log;
            
            RETURN;
        END;
        $$ LANGUAGE plpgsql;
        """)

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
